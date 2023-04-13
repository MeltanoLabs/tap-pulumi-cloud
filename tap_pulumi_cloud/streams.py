"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream


class Stacks(PulumiCloudStream):
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

    def get_child_context(
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
    ) -> dict | None:
        """Return a context object for child streams.

        Args:
            record: A record from this stream.
            context: The stream sync context.

        Returns:
            A context object for child streams.
        """
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
            th.StringType,
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
