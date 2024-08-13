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
            params["output-type"] = 'service'

        return params

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
            "info",
            th.ObjectType(
                th.Property(
                    "kind",
                    th.StringType,
                    description="The kind of update.",
                ),
                th.Property(
                    "start_time",
                    th.IntegerType,
                    description="The time the update started.",
                ),
                th.Property(
                    "message",
                    th.StringType,
                    description="The message associated with the update.",
                ),
                th.Property(
                    "environment",
                    th.ObjectType(),
                    description="The environment configuration present at the update.",
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
                th.Property(
                    "end_time",
                    th.IntegerType,
                    description="The time the update ended.",
                ),
                th.Property(
                    "resource_changes",
                    th.ObjectType(),
                    description="The resource changes associated with the update.",
                ),
            ),
            description="The information associated with the update.",
        ),

        th.Property(
            "update_id",
            th.StringType,
            description="The ID of the update.",
        ),
        th.Property(
            "github_commit_info",
            th.ObjectType(
                th.Property(
                    "slug",
                    th.StringType,
                    description="The slug of the commit.",
                ),
                th.Property(
                    "sha",
                    th.StringType,
                    description="The SHA of the commit.",
                ),
                th.Property(
                    "url",
                    th.StringType,
                    description="The URL of the commit.",
                ),
                th.Property(
                    "author",
                    th.ObjectType(
                        th.Property(
                            "name",
                            th.StringType,
                            description="The name of the author.",
                        ),
                        th.Property(
                            "github_login",
                            th.StringType,
                            description="The GitHub login of the author.",
                        ),
                        th.Property(
                            "avatar_url",
                            th.StringType,
                            description="The avatar URL of the author.",
                        ),
                    ),
                    description="The information associated with the author of the commit.",
                ),
            ),
            description="The information associated with the GitHub commit.",
        ),
        th.Property(
            "version",
            th.IntegerType,
            description="The numeric sequence of the update.",
        ),
        th.Property(
            "latest_version",
            th.IntegerType,
            description="The latest version for this stack.",
        ),
        th.Property(
            "requested_by",
            th.ObjectType(
                th.Property(
                    "name",
                    th.StringType,
                    description="The name of the requester.",
                ),
                th.Property(
                    "github_login",
                    th.StringType,
                    description="The GitHub login of the requester.",
                ),
                th.Property(
                    "avatar_url",
                    th.StringType,
                    description="The avatar URL of the requester.",
                ),
            ),
            description="The information associated with the requester.",
        ),
        th.Property(
            "policy_packs",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "name",
                        th.StringType,
                        description="The name of the policy pack.",
                    ),
                    th.Property(
                        "display_name",
                        th.StringType,
                        description="The display name of the policy pack.",
                    ),
                    th.Property(
                        "version",
                        th.IntegerType,
                        description="The version of the policy pack.",
                    ),
                    th.Property(
                        "version_tag",
                        th.StringType,
                        description="The version tag of the policy pack.",
                    ),
                    th.Property(
                        "config",
                        th.ObjectType(),
                        description="The configuration of the policy pack.",
                    ),
                ),
            ),
            description="The policy packs associated with the update.",
        ),
    ).to_dict()

    
class StackPreviews(StackUpdates):
    """Stack previews stream."""

    name = "stack_previews"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/updates/latest/previews"
    primary_keys = ["org_name", "project_name", "stack_name", "version"]
    records_jsonpath = "$.updates[*]"

    parent_stream_type = Stacks

    ## Schema same as StackUpdates, inherited


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



class StackPolicyGroups(PulumiCloudStream):
    """Stack policy groups stream."""

    name = "stack_policy_groups"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/policygroups"
    primary_keys = ["org_name", "project_name", "stack_name", "name"]
    records_jsonpath = "$.policyGroups[*]"

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
            "name",
            th.StringType,
            description="The name of the policy group.",
        ),
        th.Property(
            "is_org_default",
            th.BooleanType,
            description="Is the policy group the default for the organization.",
        ),
        th.Property(
            "num_stacks",
            th.IntegerType,
            description="The number of stacks the policy group is applied to.",
        ),
        th.Property(
            "num_enabled_policy_packs",
            th.IntegerType,
            description="The number of policy packs enabled in the policy group.",
        ),

    ).to_dict()


class StackPolicyPacks(PulumiCloudStream):
    """Stack policy groups stream."""

    name = "stack_policy_packs"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/policypacks"
    primary_keys = ["org_name", "project_name", "stack_name", "name"]
    records_jsonpath = "$.requiredPolicies[*]"

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
            "name",
            th.StringType,
            description="The name of the policy group.",
        ),
        th.Property(
            "version",
            th.IntegerType,
            description="Version of the policy pack applied to this stack.",
        ),
        th.Property(
            "versionTag",
            th.StringType,
            description="Version tag of the policy pack applied to this stack.",
        ),
        th.Property(
            "displayName",
            th.StringType,
            description="Display name of the policy pack applied to this stack.",
        ),
        th.Property(
            "packLocation",
            th.StringType,
            description="Location of the policy pack applied to this stack.",
        ),
        th.Property(
            "config",
            th.ObjectType(),
            description="The configuration of the policy pack applied to this stack.",
        ),

    ).to_dict()

class StackDeployments(PulumiCloudStream):
    """Stack deployments stream."""

    name = "stack_deployments"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/deployments"
    primary_keys = ["org_name", "project_name", "stack_name", "id"]
    records_jsonpath = "$.deployments[*]"

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
            "id",
            th.StringType,
            description="The ID of the deployment.",
        ),
        th.Property(
            "created",
            th.StringType,
            description="The time the deployment was created.",
        ),
        th.Property(
            "modified",
            th.StringType,
            description="The time the deployment was last modified.",
        ),
        th.Property(
            "status",
            th.StringType,
            description="The status of the deployment.",
        ),
        th.Property(
            "version",
            th.IntegerType,
            description="The version of the deployment.",
        ),
        th.Property(
            "requested_by",
            th.ObjectType(
                th.Property(
                    "name",
                    th.StringType,
                    description="The name of the requester.",
                ),
                th.Property(
                    "github_login",
                    th.StringType,
                    description="The GitHub login of the requester.",
                ),
                th.Property(
                    "avatar_url",
                    th.StringType,
                    description="The avatar URL of the requester.",
                ),
                th.Property(
                    "email",
                    th.StringType,
                    description="The email of the requester.",
                ),
            ),
            description="The information associated with the requester.",
        ),
        th.Property(
            "paused",
            th.BooleanType,
            description="Is the deployment paused.",
        ),
        th.Property(
            "pulumi_operation",
            th.StringType,
            description="The operation performed in the deployment.",
        ),
        th.Property(
            "updates",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "id",
                        th.StringType,
                        description="The ID of the update.",
                    ),
                    th.Property(
                        "version",
                        th.IntegerType,
                        description="The version of the update.",
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
                        "result",
                        th.StringType,
                        description="The result of the update.",
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
                        description="The environment configuration present at the update.",
                    ),
                ),
            ),
            description="The updates associated with the deployment.",
        ),
        th.Property(
            "jobs",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "status",
                        th.StringType,
                        description="The status of the job.",
                    ),
                    th.Property(
                        "started",
                        th.StringType,
                        description="The time the job started.",
                    ),
                    th.Property(
                        "last_updated",
                        th.StringType,
                        description="The time the job was last updated.",
                    ),
                    th.Property(
                        "steps",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "name",
                                    th.StringType,
                                    description="The name of the step.",
                                ),
                                th.Property(
                                    "status",
                                    th.StringType,
                                    description="The status of the step.",
                                ),
                                th.Property(
                                    "started",
                                    th.StringType,
                                    description="The time the step started.",
                                ),
                                th.Property(
                                    "last_updated",
                                    th.StringType,
                                    description="The time the step was last updated.",
                                ),
                            ),
                        ),
                        description="The steps of the job.",
                    ),
                ),
            ),
            description="The jobs associated with the deployment.",
        ),
        th.Property(
            "initiator",
            th.StringType,
            description="The initiator of the deployment.",
        ),
    ).to_dict()
