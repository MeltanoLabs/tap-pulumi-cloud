"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


class _OrgPartitionedStream(PulumiCloudStream):
    """Base class for streams that are partitioned by organization."""

    @override
    @property
    def partitions(self) -> list[dict[Any, Any]] | None:
        """List of organizations to sync."""
        return [{"org_name": org} for org in self.config["organizations"]]


class Stacks(_OrgPartitionedStream):
    """Users stream."""

    name = "stacks"
    path = "/api/user/stacks"
    primary_keys = ["org_name", "project_name", "stack_name"]
    records_jsonpath = "$.stacks[*]"

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the stack.",
        ),
        th.Property(
            "project_name",
            th.StringType,
            description="The name of the project that contains the stack.",
        ),
        th.Property(
            "stack_name",
            th.StringType,
            description="The name of the stack.",
        ),
        th.Property(
            "last_update",
            th.IntegerType,
            description="The last time the stack was updated.",
        ),
        th.Property(
            "resource_count",
            th.IntegerType,
            description="The number of resources in the stack.",
        ),
    ).to_dict()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)

        if context:
            params["organization"] = context["org_name"]

        return params

    @override
    def get_child_context(
        self,
        record: Record,
        context: Context | None,
    ) -> Context | None:
        """Return a context object for child streams."""
        return {
            "org_name": record["org_name"],
            "project_name": record["project_name"],
            "stack_name": record["stack_name"],
        }


class StackUpdates(PulumiCloudStream):
    """Stack updates stream."""

    name = "stack_updates"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/updates"
    primary_keys = ["org_name", "project_name", "stack_name", "version"]
    records_jsonpath = "$.updates[*]"

    parent_stream_type = Stacks

    schema = th.PropertiesList(
        th.Property(
            "version",
            th.IntegerType,
            description="The ID of the update.",
        ),
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the stack.",
        ),
        th.Property(
            "project_name",
            th.StringType,
            description="The name of the project that contains the stack.",
        ),
        th.Property(
            "stack_name",
            th.StringType,
            description="The name of the stack.",
        ),
        th.Property(
            "start_time",
            th.IntegerType,
            description="The time the update started.",
        ),
        th.Property(
            "end_time",
            th.IntegerType,
            description="The time the update ended.",
        ),
        th.Property(
            "kind",
            th.StringType,
            description="The kind of update.",
        ),
        th.Property(
            "message",
            th.StringType,
            description="The message associated with the update.",
        ),
        th.Property(
            "environment",
            th.ObjectType(),
            description="The environment associated with the update.",
        ),
        th.Property(
            "config",
            th.ObjectType(),
            description="The config associated with the update.",
        ),
        th.Property(
            "result",
            th.StringType,
            description="The result of the update.",
        ),
        th.Property("resource_changes", th.ObjectType()),
        th.Property("resource_count", th.IntegerType),
    ).to_dict()


class OrganizationMembers(_OrgPartitionedStream):
    """Organization members stream."""

    name = "organization_members"
    path = "/api/orgs/{org_name}/members"
    primary_keys = ["org_name", "user_name"]
    records_jsonpath = "$.members[*]"

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the stack.",
        ),
        th.Property(
            "role",
            th.StringType,
            description="The role of the user in the organization.",
        ),
        th.Property(
            "user_name",
            th.StringType,
            description="The name of the user.",
        ),
        th.Property(
            "user",
            th.ObjectType(
                th.Property(
                    "github_login",
                    th.StringType,
                    description="The GitHub login of the user.",
                ),
                th.Property(
                    "avatar_url",
                    th.StringType,
                    description="The URL of the user's avatar.",
                ),
            ),
            description="The user object.",
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The time the user was added to the organization.",
        ),
        th.Property(
            "known_to_pulumi",
            th.BooleanType,
        ),
        th.Property(
            "virtual_admin",
            th.BooleanType,
        ),
    ).to_dict()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters."""
        params = super().get_url_params(context, next_page_token)
        params["type"] = "backend"
        return params

    @override
    def post_process(
        self, row: Record, context: Context | None = None
    ) -> Record | None:
        """Post-process a row."""
        new_row = super().post_process(row, context)
        if new_row:
            new_row["user_name"] = new_row["user"].pop("name")
        return new_row


class OrganizationTeams(_OrgPartitionedStream):
    """Organization teams stream."""

    name = "organization_teams"
    path = "/api/orgs/{org_name}/teams"
    primary_keys = ["org_name", "name"]
    records_jsonpath = "$.teams[*]"

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
        ),
        th.Property(
            "kind",
            th.StringType,
        ),
        th.Property(
            "name",
            th.StringType,
        ),
        th.Property(
            "display_name",
            th.StringType,
        ),
        th.Property(
            "description",
            th.StringType,
        ),
        th.Property(
            "user_role",
            th.StringType,
        ),
    ).to_dict()
