"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import PulumiCloudStream, _OrgPartitionedStream
from tap_pulumi_cloud import stacks

class OrganizationWebhooks(_OrgPartitionedStream):
    """Stream Organization Webhooks."""

    name = "organization_webhooks"
    path = "/api/orgs/{org_name}/hooks"
    primary_keys = ["org_name", "name"]
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
    th.Property(
        "org_name",
        th.StringType,
        description="The name of the organization."
    ),
    th.Property(
        "name",
        th.StringType,
        description="The name of the webhook."
    ),
    th.Property(
        "display_name",
        th.StringType,
        description="The display name of the webhook."
    ),
    th.Property(
        "payload_url",
        th.StringType,
        description="The URL to which the webhook will send payloads."
    ),
    th.Property(
        "format",
        th.StringType,
        description="The format of the webhook payload, e.g. raw, slack, ms_teams."
    ),
    th.Property(
        "active",
        th.BooleanType,
        description="Whether the webhook is active."
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
            "webhook_name": record["name"],
            "org_name": record["org_name"],
        
        }

class OrganizationWebhookDeliveries(PulumiCloudStream):
    """Organization Webhook deliveries stream."""

    name = "organization_webhook_deliveries"
    path = "/api/orgs/{org_name}/hooks/{webhook_name}/deliveries"
    primary_keys = ["org_name", "webhook_name", "id"]
    records_jsonpath = "$[*]"

    parent_stream_type = OrganizationWebhooks

    schema = th.PropertiesList(
    th.Property(
        "org_name",
        th.StringType,
        description="The name of the organization."
    ),
    th.Property(
        "webhook_name",
        th.StringType,
        description="The name of the webhook."
    ),
    th.Property(
        "id",
        th.StringType,
        description="The ID of the delivery."
    ),
    th.Property(
        "kind",
        th.StringType,
        description="The kind of the delivery."
    ),
    th.Property(
        "payload",
        th.StringType,
        description="The payload of the delivery."
    ),
    th.Property(
        "timestamp",
        th.IntegerType,
        description="The timestamp of the delivery."
    ),
    th.Property(
        "duration",
        th.IntegerType,
        description="The duration of the delivery."
    ),
    th.Property(
        "request_url",
        th.StringType,
        description="The URL of the request."
    ),
    th.Property(
        "request_headers",
        th.StringType,
        description="The headers of the request."
    ),
    th.Property(
        "response_code",
        th.IntegerType,
        description="The response code of the delivery."
    ),
    th.Property(
        "response_headers",
        th.StringType,
        description="The headers of the response."
    ),
    th.Property(
        "response_body",
        th.StringType,
        description="The body of the response."
    )
).to_dict()



class StackWebhooks(PulumiCloudStream):
    """Stream Organization Webhooks."""

    name = "stack_webhooks"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/hooks"
    primary_keys = ["org_name", "project_name", "stack_name", "name"]
    records_jsonpath = "$[*]"

    parent_stream_type = stacks.Stacks

    schema = th.PropertiesList(
    th.Property(
        "org_name",
        th.StringType,
        description="The name of the organization."
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
        "name",
        th.StringType,
        description="The name of the webhook."
    ),
    th.Property(
        "display_name",
        th.StringType,
        description="The display name of the webhook."
    ),
    th.Property(
        "payload_url",
        th.StringType,
        description="The URL to which the webhook will send payloads."
    ),
    th.Property(
        "format",
        th.StringType,
        description="The format of the webhook payload, e.g. raw, slack, ms_teams."
    ),
    th.Property(
        "filters",
        th.ArrayType(th.StringType),
        description="The filters for the webhook."
    ),
    th.Property(
        "active",
        th.BooleanType,
        description="Whether the webhook is active."
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
            "project_name": record["project_name"],
            "stack_name": record["stack_name"],
            "webhook_name": record["name"],
        
        }
    


class StackWebhookDeliveries(PulumiCloudStream):
    """Stack Webhook deliveries stream."""

    name = "stack_webhook_deliveries"
    path = "/api/stacks/{org_name}/{project_name}/{stack_name}/hooks/{webhook_name}/deliveries"
    primary_keys = ["org_name", "project_name", "stack_name", "webhook_name", "id"]
    records_jsonpath = "$[*]"

    parent_stream_type = StackWebhooks

    schema = th.PropertiesList(
    th.Property(
        "org_name",
        th.StringType,
        description="The name of the organization."
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
        "webhook_name",
        th.StringType,
        description="The name of the webhook."
    ),
    th.Property(
        "id",
        th.StringType,
        description="The ID of the delivery."
    ),
    th.Property(
        "kind",
        th.StringType,
        description="The kind of the delivery."
    ),
    th.Property(
        "payload",
        th.StringType,
        description="The payload of the delivery."
    ),
    th.Property(
        "timestamp",
        th.IntegerType,
        description="The timestamp of the delivery."
    ),
    th.Property(
        "duration",
        th.IntegerType,
        description="The duration of the delivery."
    ),
    th.Property(
        "request_url",
        th.StringType,
        description="The URL of the request."
    ),
    th.Property(
        "request_headers",
        th.StringType,
        description="The headers of the request."
    ),
    th.Property(
        "response_code",
        th.IntegerType,
        description="The response code of the delivery."
    ),
    th.Property(
        "response_headers",
        th.StringType,
        description="The headers of the response."
    ),
    th.Property(
        "response_body",
        th.StringType,
        description="The body of the response."
    )
).to_dict()