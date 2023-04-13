"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_pulumi_cloud.tap import TapPulumiCloud

SAMPLE_CONFIG: dict[str, Any] = {}

# Run standard built-in tap tests from the SDK:
TestTapPulumiCloud = get_tap_test_class(
    TapPulumiCloud,
    suite_config=SuiteConfig(max_records_limit=10),
)
