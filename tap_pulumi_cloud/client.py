"""REST client handling, including PulumiCloudStream base class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

import humps
from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers._typing import TypeConformanceLevel

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


class PulumiCloudStream(RESTStream[str]):
    """Pulumi Cloud stream class."""

    url_base = "https://api.pulumi.com"
    next_page_token_jsonpath = "$.continuationToken"  # noqa: S105

    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return APIKeyAuthenticator(
            key="Authorization",
            value=f"token {token}",
            location="header",
        )

    @override
    @property
    def http_headers(self) -> dict[str, str]:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "User-Agent": f"{self.tap_name}/{self._tap.plugin_version}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.pulumi+8",
        }

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict[str, Any] = {}
        if next_page_token:
            params["continuationToken"] = next_page_token
        return params

    @override
    def post_process(
        self,
        row: Record,
        context: Context | None = None,
    ) -> Record | None:
        """Post-process a row of data."""
        return humps.decamelize(row)
