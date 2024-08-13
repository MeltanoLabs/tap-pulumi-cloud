"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream


class OrganizationMembers(_OrgPartitionedStream):
    """Organization members stream."""

    name = "organization_members"
    path = "/api/orgs/{org_name}/members"
    primary_keys = ["org_name", "user_github_login"]
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
            "user_github_login",
            th.StringType,
            description="The github login of the user.",
        ),
        th.Property(
            "user_name",
            th.StringType,
            description="The name of the user.",
        ),
        th.Property(
            "user_avatar_url",
            th.StringType,
            description="The name of the user.",
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
            new_row["user_github_login"] = new_row["user"].pop("github_login")
            new_row["user_avatar_url"] = new_row["user"].pop("avatar_url")
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
            description="The name of the organization that owns the team.",
        ),
        th.Property(
            "kind",
            th.StringType,
            description="The kind of team.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The name of the team.",
        ),
        th.Property(
            "display_name",
            th.StringType,
            description="The display name of the team.",
        ),
        th.Property(
            "description",
            th.StringType,
            description="The description of the team.",
        ),
        th.Property(
            "user_role",
            th.StringType,
            description="The default user role of the team members.",
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


class OrganizationTeamsMembers(PulumiCloudStream):
    """Organization team members stream."""

    name = "organization_team_members"
    path = "/api/orgs/{org_name}/teams/{team_name}"
    primary_keys = ["org_name", "team_name", "github_login"]
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

class OrganizationTeamsStacks(PulumiCloudStream):
    """Organization team stacks stream."""

    name = "organization_team_stacks"
    path = "/api/orgs/{org_name}/teams/{team_name}"
    primary_keys = ["org_name", "team_name", "project_name", "stack_name"]
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

class OrganizationTeamsEnvironments(PulumiCloudStream):
    """Organization team environments stream."""

    name = "organization_team_environments"
    path = "/api/orgs/{org_name}/teams/{team_name}"
    primary_keys = ["org_name", "team_name", "env_name"]
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

class OrganizationTeamsAccessTokens(PulumiCloudStream):
    """Organization team access tokens stream."""

    name = "organization_team_access_tokens"
    path = "/api/orgs/{org_name}/teams/{team_name}/tokens"
    primary_keys = ["org_name", "team_name", "id"]
    records_jsonpath = "$.tokens[*]"

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

class OrganizationOidcIssuers(_OrgPartitionedStream):
    """Organization OIDC issuers stream."""

    name = "organization_oidc_issuers"
    path = "/api/orgs/{org_name}/oidc/issuers"
    primary_keys = ["org_name", "id"]
    records_jsonpath = "$.oidcIssuers[*]"

    schema = th.PropertiesList(
    th.Property(
        "org_name",
        th.StringType,
        ),
    th.Property(
        "id",
        th.StringType,
        description="The unique identifier for the Issuer."
    ),
    th.Property(
        "name",
        th.StringType,
        description="The name of the Issuer."
    ),
    th.Property(
        "url",
        th.StringType,
        description="The issuer URL."
    ),
    th.Property(
        "issuer",
        th.StringType,
        description="The issuer URL"
    ),
    th.Property(
        "created",
        th.DateTimeType,
        description="The timestamp when the Issuer was created."
    ),
    th.Property(
        "modified",
        th.DateTimeType,
        description="The timestamp when the Issuer was last modified."
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
            "org_name": record["org_name"],
            "issuer_id": record["id"],
        }

class OrganizationOidcIssuersPolicies(PulumiCloudStream):
    """OIDC Issuer Policy details Stream."""

    name = "organization_oidc_issuers_policies"
    path = "/api/orgs/{org_name}/auth/policies/oidcissuers/{issuer_id}"
    primary_keys = ["org_name", "issuer_id", "id"]
    parent_stream_type = OrganizationOidcIssuers



    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
        ),
        th.Property(
            "issuer_id",
            th.StringType,
            description="The unique identifier for the OIDC Issuer."
        ),
        th.Property(
            "id",
            th.StringType,
            description="The unique identifier for the policy."
        ),
        th.Property(
            "version",
            th.IntegerType,
            description="The version number of the policy."
        ),
        th.Property(
            "created",
            th.DateTimeType,
            description="The timestamp when the policy was created."
        ),
        th.Property(
            "modified",
            th.DateTimeType,
            description="The timestamp when the policy was last modified."
        ),
        th.Property(
            "policies",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "decision",
                        th.StringType,
                        description="The decision made by the policy, e.g., 'allow' or 'deny'."
                    ),
                    th.Property(
                        "tokenType",
                        th.StringType,
                        description="The type of token associated with the policy."
                    ),
                    th.Property(
                        "authorizedPermissions",
                        th.ArrayType(
                            th.StringType
                        ),
                    description="The permissions authorized by the policy."
                ),
                    th.Property(
                        "rules",
                        th.ObjectType(
                            th.Property(
                                "*",  # Wildcard to allow for any key in the rules object
                                th.StringType
                            )
                        ),
                        description="Dynamic set of rules applied by the policy."
                    )
                )
            ),
            description="List of policies within the OIDC Issuer."
        )
    ).to_dict()


class OrganizationAgentPools(_OrgPartitionedStream):
    """Organization Agent Pools Stream."""

    name = "organization_agent_pools"
    path = "/api/orgs/{org_name}/agent-pools"
    primary_keys = ["org_name", "id"]
    records_jsonpath = "$.agentPools[*]"


    schema = th.PropertiesList(
    th.Property(
        "org_name",
        th.StringType,
        description="The name of the Agent Pool organization.",
        ),
    th.Property(
        "created",
        th.IntegerType,
        description="The timestamp when the Agent Pool was created, in milliseconds - epoch."
    ),
    th.Property(
        "id",
        th.StringType,
        description="The unique identifier for the Agent Pool."
    ),
    th.Property(
        "name",
        th.StringType,
        description="The Agent Pool name."
    ),
    th.Property(
        "description",
        th.StringType,
        description="The Agent Pool description."
    ),
    th.Property(
        "last_seen",
        th.IntegerType,
        description="The timestamp when the Agent Pool was seen for the last time, in milliseconds - epoch."
    ),
    th.Property(
        "status",
        th.StringType,
        description="The current status of the Agent Pool."
    ),
    th.Property(
        "last_deployment",
        th.StringType,
        description="The last deployment associated with the Agent Pool.",
        required=False
    )
).to_dict()




