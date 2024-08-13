"""Stream type classes for tap-pulumi-cloud."""
from __future__ import annotations

import typing as t

from datetime import datetime
from requests import Response
from singer_sdk import typing as th


from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream
from singer_sdk.pagination import (
    BaseAPIPaginator
)

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.helpers.types import Context
from singer_sdk import metrics


class AuditLogsPaginator(BaseAPIPaginator[t.Optional[str]]):
    """Paginator class for APIs returning a pagination token in the response body."""

    def __init__(
        self,
        jsonpath: str,
        since: int,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
        """Create a new paginator.

        Args:
            jsonpath: A JSONPath expression.
            args: Paginator positional arguments for base class.
            kwargs: Paginator keyword arguments for base class.
        """
        super().__init__(None, *args, **kwargs)
        self._jsonpath = jsonpath
        self._since = since

    def get_next(self, response: Response) -> str | None:
        """Get the next page token.

        Args:
            response: API response object.

        Returns:
            The next page token.
        """
        all_matches = extract_jsonpath(self._jsonpath, response.json())
        matched = next(all_matches, None)
        if matched is None or int(matched) < self._since:
            return None
        return matched

class AuditLogs(_OrgPartitionedStream):
    """Stream Audit Logs."""

    name = "audit_logs"
    path = "/api/orgs/{org_name}/auditlogs"
    primary_keys = ["org_name", "timestamp", "event", "description"]
    records_jsonpath = "$.auditLogEvents[*]"
    replication_key = "timestamp"
    is_sorted = False

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization."
        ),
        th.Property(
            "timestamp",
            th.DateTimeType,
            description="The timestamp of the audit log event."
        ),
        th.Property(
            "source_ip",
            th.StringType,
            description="The source IP of the audit log event."
        ),
        th.Property(
            "event",
            th.StringType,
            description="The event of the audit log event."
        ),
        th.Property(
            "description",
            th.StringType,
            description="The description of the audit log event."
        ),
        th.Property(
            "user",
            th.ObjectType(
                th.Property(
                    "name",
                    th.StringType,
                    description="The name of the user."
                ),
                th.Property(
                    "github_login",
                    th.StringType,
                    description="The GitHub login of the user."
                ),
                th.Property(
                    "avatar_url",
                    th.StringType,
                    description="The avatar URL of the user."
                )
            ),
            description="The user of the audit log event."
        ),
        th.Property(
            "token_id",
            th.StringType,
            description="The token id associated with this event."
        ),
        th.Property(
            "token_name",
            th.StringType,
            description="The token name associated with this event."
        ),
        th.Property(
            "req_org_admin",
            th.BooleanType,
            description="Required organization admin role."
        ),
        th.Property(
            "req_stack_admin",
            th.BooleanType,
            description="Required stack admin role."
        ),
        th.Property(
            "auth_failure",
            th.BooleanType,
            description="Event was the result of an authentication check failure."
        ),
    ).to_dict()

    def first_timestamp(self, context):
        return self.get_starting_timestamp(context).timestamp()

    def get_new_paginator(self, context: Context | None) -> BaseAPIPaginator:
        return AuditLogsPaginator(self.next_page_token_jsonpath, self.first_timestamp(context))
    
    def request_records(self, context: Context | None) -> t.Iterable[dict]:
        """Request records from REST endpoint(s), returning response records.

        If pagination is detected, pages will be recursed automatically.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            An item for every record in the response.
        """
        paginator = self.get_new_paginator(context)
        decorated_request = self.request_decorator(self._request)
        pages = 0

        with metrics.http_request_counter(self.name, self.path) as request_counter:
            request_counter.context = context

            while not paginator.finished:
                prepared_request = self.prepare_request(
                    context,
                    next_page_token=paginator.current_value,
                )
                resp = decorated_request(prepared_request, context)
                request_counter.increment()
                self.update_sync_costs(prepared_request, resp, context)
                records = iter(self.parse_response(resp))
                try:
                    first_record = next(records)
                except StopIteration:
                    self.logger.info(
                        "Pagination stopped after %d pages because no records were "
                        "found in the last response",
                        pages,
                    )
                    break
                yield first_record
                yield from records
                pages += 1

                paginator.advance(resp)

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of URL query parameters.

        Args:
            context: The stream sync context.
            next_page_token: A token for the next page of results.

        Returns:
            A dictionary of URL query parameters.
        """
        params = {'pageSize': 100}
        since = round(self.first_timestamp(context))
        if next_page_token:
            until = next_page_token
        else:
            until = round(self.get_replication_key_signpost(context).timestamp())
        params["startTime"] = since
        params["endTime"] = until
        return params


    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Post-process a row of data."""
        row = super().post_process(row, context)
        row["timestamp"] = datetime.fromtimestamp(row["timestamp"])
        return row