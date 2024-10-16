"""REST client handling, including PulumiCloudStream base class."""

from __future__ import annotations

import typing as t
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import requests
import humps
from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.helpers._typing import TypeConformanceLevel


class PulumiCloudStream(RESTStream):
    """Pulumi Cloud stream class."""

    url_base = "https://api.pulumi.com"
    next_page_token_jsonpath = "$.continuationToken"  # noqa: S105
    tolerated_http_errors: t.Sequence[int] = []

    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=f"token {token}",
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "User-Agent": f"{self.tap_name}/{self._tap.plugin_version}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.pulumi+8",
        }

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict = {"pageSize": 100}
        if next_page_token:
            params["continuationToken"] = next_page_token
        return params

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Post-process a row of data."""
        return humps.decamelize(row)

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: A raw :class:`requests.Response`

        Yields:
            One item for every item found in the response.
        """
        if response.status_code in self.tolerated_http_errors:
            return []
        return super().parse_response(response)

    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response.

        Checks for error status codes and whether they are fatal or retriable.

        In case an error is deemed transient and can be safely retried, then this
        method should raise an :class:`singer_sdk.exceptions.RetriableAPIError`.
        By default this applies to 5xx error codes, along with values set in:
        :attr:`~singer_sdk.RESTStream.extra_retry_statuses`

        In case an error is unrecoverable raises a
        :class:`singer_sdk.exceptions.FatalAPIError`. By default, this applies to
        4xx errors, excluding values found in:
        :attr:`~singer_sdk.RESTStream.extra_retry_statuses`

        Tap developers are encouraged to override this method if their APIs use HTTP
        status codes in non-conventional ways, or if they communicate errors
        differently (e.g. in the response body).

        .. image:: ../images/200.png

        Args:
            response: A :class:`requests.Response` object.

        Raises:
            FatalAPIError: If the request is not retriable.
            RetriableAPIError: If the request is retriable.
        """
        if response.status_code in self.tolerated_http_errors:
            msg = (
                f"{response.status_code} Tolerated Status Code "
                f"(Reason: {response.reason}) for path: {response.request.url}"
            )
            self.logger.info(msg)
            return

        if (
            response.status_code in self.extra_retry_statuses
            or response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR
        ):
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)

        if (
            HTTPStatus.BAD_REQUEST
            <= response.status_code
            < HTTPStatus.INTERNAL_SERVER_ERROR
        ):
            msg = self.response_error_message(response)
            raise FatalAPIError(msg)


class _OrgPartitionedStream(PulumiCloudStream):
    """Base class for streams that are partitioned by organization."""

    @property
    def partitions(self) -> list[dict] | None:
        """List of organizations to sync."""
        return [{"org_name": org} for org in self.config["organizations"]]
