"""Tap executable."""

from __future__ import annotations

from tap_pulumi_cloud.tap import TapPulumiCloud

TapPulumiCloud.cli()
