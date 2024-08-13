"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream


class PolicyGroupsList(_OrgPartitionedStream):
    """Auxiliar stream to get Organization Policy Groups names."""

    name = "policy_groups_list"
    path = "/api/orgs/{org_name}/policygroups"
    primary_keys = ["org_name", "name"]
    records_jsonpath = "$.policyGroups[*]"
    selected_by_default = False

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
        ),
        th.Property(
            "name",
            th.StringType,
        ),
        th.Property(
            "is_org_default",
            th.BooleanType,
        ),
        th.Property(
            "num_stacks",
            th.IntegerType,
        ),
        th.Property(
            "num_enabled_policy_packs",
            th.IntegerType,
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
            "policy_group_name": record["name"],
            "org_name": record["org_name"],
            "num_enabled_policy_packs": record["num_enabled_policy_packs"],
            "num_stacks": record["num_stacks"],
        }


class PolicyGroups(PulumiCloudStream):
    """Organization Policy Groups."""

    name = "policy_groups"
    path = "/api/orgs/{org_name}/policygroups/{policy_group_name}"
    primary_keys = ["org_name", "policy_group_name"]
    

    parent_stream_type = PolicyGroupsList

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The Organization name.",
        ),
        th.Property(
            "policy_group_name",
            th.StringType,
            description="The Policy group name.",
        ),
        th.Property(
            "num_stacks",
            th.IntegerType,
            description="The amount of stacks asociated to the policy group.",
        ),
        th.Property(
            "num_enabled_policy_packs",
            th.IntegerType,
            description="The amount of enabled Policy Packs in the Policy Group .",
        ),
        th.Property(
            "is_org_default",
            th.BooleanType,
        ),
         th.Property(
        "applied_policy_packs",
        th.ArrayType(
            th.ObjectType(
                th.Property("name", th.StringType),
                th.Property("displayName", th.StringType),
                th.Property("version", th.IntegerType),
                th.Property("versionTag", th.StringType),
                th.Property(
                    "config",
                    th.ObjectType(
                        th.Property(
                            "all",
                            th.ObjectType(
                                th.Property("enforcementLevel", th.StringType)
                            )
                        ),
                        th.Property(
                            "prohibited-public-internet",
                            th.ObjectType(
                                th.Property("enforcementLevel", th.StringType)
                            )
                        ),
                        th.Property(
                            "s3-bucket-replication-enabled",
                            th.ObjectType(
                                th.Property("enforcementLevel", th.StringType)
                            )
                        ),
                        th.Property(
                            "s3-no-public-read",
                            th.ObjectType(
                                th.Property("enforcementLevel", th.StringType)
                            )
                        )
                    )
                )
            )
        ),
        description="Policy Packs list with configuration details.",
        ),
    ).to_dict()

    


class PolicyPacks(_OrgPartitionedStream):
    """Policy Packs, versions and version tags"""

    path = "/api/orgs/{org_name}/policypacks"
    name = "policy_packs"
    primary_keys = ["org_name", "name"]
    records_jsonpath = "$.policyPacks[*]"
    selected_by_default = False

    schema = th.PropertiesList(
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
        "versions",
        th.ArrayType(
            th.IntegerType
        ),
        description="List of versions available for the policy pack.",
    ),
    th.Property(
        "version_tags",
        th.ArrayType(
            th.StringType
        ),
        description="List of version tags corresponding to the versions.",
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
            "policy_pack_name": record["name"],
            "org_name": record["org_name"],
        }


class LatestPolicyPacks(PulumiCloudStream):
    """Latest Policy Pack with complete Policy details."""
    

    name = "policy_pack_detailed"
    path = "/api/orgs/{org_name}/policypacks/{policy_pack_name}/latest"

    """Version is included in the primary key, so when a new version is created,
      the latest status of the older versions will be retained."""
    primary_keys = ["org_name", "policy_pack_name", "version"]
    

    parent_stream_type = PolicyPacks

    schema = th.PropertiesList(
    th.Property(
        "name",
        th.StringType,
        description="The name of the policy pack."
    ),
    th.Property(
        "display_name",
        th.StringType,
        description="The display name of the policy pack."
    ),
    th.Property(
        "version",
        th.IntegerType,
        description="The version of the policy pack."
    ),
    th.Property(
        "version_tag",
        th.StringType,
        description="The version tag of the policy pack."
    ),
    th.Property(
        "policies",
        th.ArrayType(
            th.ObjectType(
                th.Property(
                    "name",
                    th.StringType,
                    description="The name of the policy."
                ),
                th.Property(
                    "displayName",
                    th.StringType,
                    description="The display name of the policy."
                ),
                th.Property(
                    "description",
                    th.StringType,
                    description="A description of the policy."
                ),
                th.Property(
                    "enforcementLevel",
                    th.StringType,
                    description="The enforcement level of the policy."
                ),
                th.Property(
                    "message",
                    th.StringType,
                    description="The message associated with the policy."
                ),
                th.Property(
                    "configSchema",
                    th.ObjectType(
                        th.Property(
                            "properties",
                            th.ObjectType(
                                th.Property(
                                    "enforcementLevel",
                                    th.ObjectType(
                                        th.Property(
                                            "enum",
                                            th.ArrayType(
                                                th.StringType
                                            ),
                                            description="possible enforcement levels."
                                        ),
                                        th.Property(
                                            "type",
                                            th.StringType,
                                            description="The type of the enforcement Level."
                                        )
                                    )
                                )
                            )
                        ),
                        th.Property(
                            "type",
                            th.StringType,
                            description="The type of the config schema."
                        )
                    ),
                    description="Configuration schema for the policy."
                )
            )
        ),
        description="List of policies within the policy pack."
    ),
    th.Property(
        "applied",
        th.BooleanType,
        description="Indicates whether the policy pack is applied."
    ),
).to_dict()

