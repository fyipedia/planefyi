"""HTTP API client for planefyi.com REST endpoints.

Requires the ``api`` extra: ``pip install planefyi[api]``

Usage::

    from planefyi.api import PlaneFYI

    with PlaneFYI() as api:
        items = api.list_aircraft_families()
        detail = api.get_aircraft_family("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class PlaneFYI:
    """API client for the planefyi.com REST API.

    Provides typed access to all planefyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://planefyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://planefyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_aircraft_families(self, **params: Any) -> dict[str, Any]:
        """List all aircraft families."""
        return self._get("/api/v1/aircraft-families/", **params)

    def get_aircraft_family(self, slug: str) -> dict[str, Any]:
        """Get aircraft family by slug."""
        return self._get(f"/api/v1/aircraft-families/" + slug + "/")

    def list_aircraft_systems(self, **params: Any) -> dict[str, Any]:
        """List all aircraft systems."""
        return self._get("/api/v1/aircraft-systems/", **params)

    def get_aircraft_system(self, slug: str) -> dict[str, Any]:
        """Get aircraft system by slug."""
        return self._get(f"/api/v1/aircraft-systems/" + slug + "/")

    def list_aircraft_types(self, **params: Any) -> dict[str, Any]:
        """List all aircraft types."""
        return self._get("/api/v1/aircraft-types/", **params)

    def get_aircraft_type(self, slug: str) -> dict[str, Any]:
        """Get aircraft type by slug."""
        return self._get(f"/api/v1/aircraft-types/" + slug + "/")

    def list_airlines(self, **params: Any) -> dict[str, Any]:
        """List all airlines."""
        return self._get("/api/v1/airlines/", **params)

    def get_airline(self, slug: str) -> dict[str, Any]:
        """Get airline by slug."""
        return self._get(f"/api/v1/airlines/" + slug + "/")

    def list_aviation_terms(self, **params: Any) -> dict[str, Any]:
        """List all aviation terms."""
        return self._get("/api/v1/aviation-terms/", **params)

    def get_aviation_term(self, slug: str) -> dict[str, Any]:
        """Get aviation term by slug."""
        return self._get(f"/api/v1/aviation-terms/" + slug + "/")

    def list_engine_profiles(self, **params: Any) -> dict[str, Any]:
        """List all engine profiles."""
        return self._get("/api/v1/engine-profiles/", **params)

    def get_engine_profile(self, slug: str) -> dict[str, Any]:
        """Get engine profile by slug."""
        return self._get(f"/api/v1/engine-profiles/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_fleet(self, **params: Any) -> dict[str, Any]:
        """List all fleet."""
        return self._get("/api/v1/fleet/", **params)

    def get_fleet(self, slug: str) -> dict[str, Any]:
        """Get fleet by slug."""
        return self._get(f"/api/v1/fleet/" + slug + "/")

    def list_manufacturers(self, **params: Any) -> dict[str, Any]:
        """List all manufacturers."""
        return self._get("/api/v1/manufacturers/", **params)

    def get_manufacturer(self, slug: str) -> dict[str, Any]:
        """Get manufacturer by slug."""
        return self._get(f"/api/v1/manufacturers/" + slug + "/")

    def list_seat_maps(self, **params: Any) -> dict[str, Any]:
        """List all seat maps."""
        return self._get("/api/v1/seat-maps/", **params)

    def get_seat_map(self, slug: str) -> dict[str, Any]:
        """Get seat map by slug."""
        return self._get(f"/api/v1/seat-maps/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> PlaneFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
