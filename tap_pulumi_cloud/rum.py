"""Stream type classes for tap-pulumi-cloud."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_pulumi_cloud.client import _OrgPartitionedStream


class RumUsageDaily(_OrgPartitionedStream):
    """RUM Usage Stream."""

    name = "daily_rum_usage"
    path = "/api/orgs/{org_name}/resources/summary?granularity=daily&lookbackDays=365"
    primary_keys: t.Sequence[str] = ["org_name", "year", "month", "day"]
    records_jsonpath = "$.summary[*]"

    schema = th.PropertiesList(
        th.Property(
            "org_name",
            th.StringType,
        ),
        th.Property("year", th.IntegerType, description="The year of the RUM usage."),
        th.Property("month", th.IntegerType, description="The month of the RUM usage."),
        th.Property("day", th.IntegerType, description="The day of the RUM usage."),
        th.Property("resources", th.IntegerType, description="Daily RUM usage."),
        th.Property("resourceHours", th.IntegerType, description="Hourly RUM usage."),
    ).to_dict()
