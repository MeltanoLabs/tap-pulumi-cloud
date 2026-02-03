"""Pulumi Cloud tap class."""

from __future__ import annotations

import sys
from typing import Any

import requests_cache
from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_pulumi_cloud import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapPulumiCloud(Tap):
    """Singer tap for Pulumi Cloud."""

    name = "tap-pulumi-cloud"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            secret=True,
            description="API Token for Pulumi Cloud",
        ),
        th.Property(
            "organizations",
            th.ArrayType(th.StringType),  # ty: ignore[invalid-argument-type]
            description="List of organizations to sync",
            required=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
        th.Property(
            "requests_cache",
            th.ObjectType(
                th.Property(
                    "enabled",
                    th.BooleanType,
                    default=False,
                    description="Enable requests cache",
                ),
                th.Property(
                    "config",
                    th.ObjectType(
                        th.Property(
                            "expire_after",
                            th.IntegerType,
                            description="Cache expiration time in seconds",
                        ),
                    ),
                    description="Requests cache configuration",
                    default={},
                ),
            ),
            description="Cache configuration for HTTP requests",
        ),
        th.Property(
            "enterprise_streams",
            th.BooleanType,
            description="Whether to include enterprise streams",
            default=False,
        ),
        additional_properties=False,
    ).to_dict()

    @override
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the tap."""
        super().__init__(*args, **kwargs)

        if self.config.get("requests_cache", {}).get("enabled", False):
            requests_cache.install_cache(
                "requests_cache",
                **self.config["requests_cache"].get("config", {}),
            )

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Pulumi Cloud streams.
        """
        pulumi_streams = [
            streams.Stacks(tap=self),
            streams.StackUpdates(tap=self),
        ]

        if self.config["enterprise_streams"]:
            pulumi_streams.extend(
                [
                    streams.OrganizationTeams(tap=self),
                    streams.OrganizationMembers(tap=self),
                ]
            )

        return pulumi_streams
