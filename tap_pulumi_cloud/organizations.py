"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream


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
        params = super().get_url_params(context, next_page_token)
        params["type"] = "backend"
        return params

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """Post-process a row.

        Args:
            row: A row.
            context: The stream sync context.

        Returns:
            The processed row.
        """
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
