"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream


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

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
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

class StackDetails(PulumiCloudStream):
    """Stack details stream."""

    name = "stack_details"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}"
    primary_keys = ["org_name", "project_name", "stack_name"]
    parent_stream_type = Stacks

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
            "current_operation",
            th.ObjectType(
                th.Property(
                    "kind",
                    th.StringType,
                    description="The kind of operation.",
                ),
                th.Property(
                    "author",
                    th.StringType,
                    description="The author of the operation.",
                ),
                th.Property(
                    "started",
                    th.IntegerType,
                    description="The time the operation started.",
                ),
            ),
            description="The name of the current operation being ran.",
        ),
        th.Property(
            "active_update",
            th.StringType,
            description="The ID of the active update.",
        ),
        th.Property(
            "tags",
            th.ObjectType(),
            description="The tags associated with the stack.",
        ),
        th.Property(
            "stack_name",
            th.StringType,
            description="The name of the stack.",
        ),
        th.Property(
            "version",
            th.IntegerType,
            description="The ID of the update.",
        )
    ).to_dict()
    

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
            "update_id",
            th.IntegerType,
            description="The internal ID of the update.",
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


class StackResources(PulumiCloudStream):
    """Stack resources stream."""

    name = "stack_resources"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/export"
    primary_keys = ["org_name", "project_name", "stack_name", "urn"]
    records_jsonpath = "$.deployment.resources[*]"

    parent_stream_type = Stacks

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
            "urn",
            th.StringType,
            description="The URN of the resource.",
        ),
        th.Property(
            "type",
            th.StringType,
            description="The type of the resource.",
        ),
        th.Property(
            "id",
            th.StringType,
            description="The ID of the resource.",
        ),
        th.Property(
            "custom",
            th.BooleanType,
            description="Is it a custom resource?; a cloud resource managed by a resource provider such as AWS, Microsoft Azure, Google Cloud or Kubernetes.",
        ),
        th.Property(
            "created",
            th.StringType,
            description="The time the resource was created.",
        ),
        th.Property(
            "modified",
            th.StringType,
            description="The time the resource was last modified.",
        ),
        th.Property(
            "inputs",
            th.ObjectType(),
            description="The inputs used for this resource.",
        ),
        th.Property(
            "outputs",
            th.ObjectType(),
            description="The outputs generated by this resource.",
        ),
        th.Property(
            "protect",
            th.StringType,
            description="The resource is protected for deletion",
        ),
        th.Property(
            "dependencies",
            th.ArrayType(th.StringType),
            description="The dependencies of the resource.",
        ),
        th.Property(
            "parent",
            th.StringType,
            description="Parent resource of this resource.",
        ),        
        th.Property(
            "property_dependencies",
            th.ObjectType(),
            description="The property dependencies of the resource.",
        ),
    ).to_dict()
