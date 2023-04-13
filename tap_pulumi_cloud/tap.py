"""Pulumi Cloud tap class."""

from __future__ import annotations

import typing as t

import requests_cache
from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_pulumi_cloud import streams


class TapPulumiCloud(Tap):
    """Singer tap for Pulumi Cloud."""

    name = "tap-pulumi-cloud"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Pulumi Cloud",
        ),
        th.Property(
            "organizations",
            th.ArrayType(th.StringType),
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
        additional_properties=False,
    ).to_dict()

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Initialize the tap."""
        super().__init__(*args, **kwargs)

        if self.config.get("requests_cache", {}).get("enabled", False):
            requests_cache.install_cache(
                "requests_cache",
                **self.config["requests_cache"].get("config", {}),
            )

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Pulumi Cloud streams.
        """
        return [
            streams.Stacks(tap=self),
            streams.StackUpdates(tap=self),
            streams.OrganizationMembers(tap=self),
            streams.OrganizationTeams(tap=self),
        ]
