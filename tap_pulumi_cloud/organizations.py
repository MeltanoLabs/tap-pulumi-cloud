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
            "team_name": record["name"]
        }


class OrganizationTeamsMembers(_OrgPartitionedStream):
    """Organization team members stream."""

    name = "organization_team_members"
    path = "/api/orgs/{org_name}/teams/{team_name}"
    primary_keys = ["org_name", "team_name"]
    records_jsonpath = "$.members[*]"

    parent_stream_type = OrganizationTeams

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the team.",
        ),
        th.Property(
            "team_name",
            th.StringType,
            description="The name of the team.",
        ),
        th.Property(
            "role",
            th.StringType,
            description="The role of the user in the team.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The name of the user.",
        ),
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
    ).to_dict()

class OrganizationTeamsStacks(_OrgPartitionedStream):
    """Organization team stacks stream."""

    name = "organization_team_stacks"
    path = "/api/orgs/{org_name}/teams/{team_name}"
    primary_keys = ["org_name", "team_name"]
    records_jsonpath = "$.stacks[*]"

    parent_stream_type = OrganizationTeams

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the team.",
        ),
        th.Property(
            "team_name",
            th.StringType,
            description="The name of the team.",
        ),
        th.Property(
            "project_name",
            th.StringType,
            description="The name of the project.",
        ),
        th.Property(
            "stack_name",
            th.StringType,
            description="The name of the stack.",
        ),
        th.Property(
            "permissions",
            th.IntegerType,
            description="Permissions for the stack: None = 0, Read = 101, Write = 102, Admin = 103.",
        ),
    ).to_dict()

class OrganizationTeamsEnvironments(_OrgPartitionedStream):
    """Organization team environments stream."""

    name = "organization_team_environments"
    path = "/api/orgs/{org_name}/teams/{team_name}"
    primary_keys = ["org_name", "team_name"]
    records_jsonpath = "$.environments[*]"

    parent_stream_type = OrganizationTeams

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the team.",
        ),
        th.Property(
            "team_name",
            th.StringType,
            description="The name of the team.",
        ),
        th.Property(
            "project_name",
            th.StringType,
            description="The name of the project.",
        ),
        th.Property(
            "env_name",
            th.StringType,
            description="The name of the environment.",
        ),
        th.Property(
            "permission",
            th.StringType,
            description="Permissions for the environment.",
        ),
    ).to_dict()

class OrganizationAccessTokens(_OrgPartitionedStream):
    """Organization access tokens stream."""

    name = "organization_access_tokens"
    path = "/api/orgs/{org_name}/tokens"
    primary_keys = ["org_name", "id"]
    records_jsonpath = "$.tokens[*]"

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
            description="The name of the organization that owns the token.",
        ),
        th.Property(
            "id",
            th.StringType,
            description="The ID of the token.",
        ),
        th.Property(
            "description",
            th.StringType,
            description="The description of the token.",
        ),
        th.Property(
            "expires",
            th.IntegerType,
            description="The expiration time of the token.",
        ),
        th.Property(
            "last_used",
            th.IntegerType,
            description="The time the token was last used.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The name of the token"
        ),
    ).to_dict()

