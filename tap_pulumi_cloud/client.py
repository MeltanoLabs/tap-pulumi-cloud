"""REST client handling, including PulumiCloudStream base class."""

from __future__ import annotations

from typing import Any

import humps
from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers._typing import TypeConformanceLevel


class PulumiCloudStream(RESTStream):
    """Pulumi Cloud stream class."""

    url_base = "https://api.pulumi.com"
    next_page_token_jsonpath = "$.continuationToken"  # noqa: S105

    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=f"token {token}",
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "User-Agent": f"{self.tap_name}/{self._tap.plugin_version}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.pulumi+8",
        }

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["continuationToken"] = next_page_token
        return params

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Post-process a row of data."""
        return humps.decamelize(row)
