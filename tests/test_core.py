"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_pulumi_cloud.tap import TapPulumiCloud

SAMPLE_CONFIG: dict[str, Any] = {}

# Run standard built-in tap tests from the SDK:
TestTapPulumiCloud = get_tap_test_class(
    TapPulumiCloud,
    config={},
    suite_config=SuiteConfig(
        # TODO(edgarrmondragon): Parent streams are evaluated before any records are
        # emitted because child records are emitted first. This causes the tests to fail
        # because no parent records are detected. This is a bug in the SDK.
        # https://github.com/MeltanoLabs/tap-pulumi-cloud/issues/72
        # max_records_limit=10,  # noqa: ERA001
        ignore_no_records_for_streams=["organization_teams"],
    ),
)
