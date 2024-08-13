"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream


class Environments(_OrgPartitionedStream):
    """Stream Organization Environments."""

    name = "environments"
    path = "/api/preview/environments/{org_name}"
    primary_keys = ["org_name", "name"]
    records_jsonpath = "$.environments[*]"

    schema = th.PropertiesList(
    th.Property(
        "project",
        th.StringType,
        description="The project associated with this environment."
    ),
    th.Property(
        "name",
        th.StringType,
        description="The name of the environment."
    ),
    th.Property(
        "created",
        th.DateTimeType,
        description="The timestamp when the environment was created."
    ),
    th.Property(
        "modified",
        th.DateTimeType,
        description="The timestamp when the environment was last modified."
    ),
    th.Property(
        "tags",
        th.ObjectType(
            th.Property(
                "*",  # Wildcard to allow for any key in the tags object
                th.StringType
            )
        ),
        description="A dictionary of tags associated with the environment, allowing dynamic keys."
    )
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
            "environment_name": record["name"],
            "org_name": record["org_name"],
        
        }


