"""MCP server for planefyi — AI assistant tools for planefyi.com.

Run: uvx --from "planefyi[mcp]" python -m planefyi.mcp_server
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PlaneFYI")


@mcp.tool()
def list_aircraft_types(limit: int = 20, offset: int = 0) -> str:
    """List aircraft_types from planefyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from planefyi.api import PlaneFYI

    with PlaneFYI() as api:
        data = api.list_aircraft_types(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No aircraft_types found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def get_aircraft_type(slug: str) -> str:
    """Get detailed information about a specific aircraft_type.

    Args:
        slug: URL slug identifier for the aircraft_type.
    """
    from planefyi.api import PlaneFYI

    with PlaneFYI() as api:
        data = api.get_aircraft_type(slug)
        return str(data)


@mcp.tool()
def list_manufacturers(limit: int = 20, offset: int = 0) -> str:
    """List manufacturers from planefyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from planefyi.api import PlaneFYI

    with PlaneFYI() as api:
        data = api.list_manufacturers(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No manufacturers found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def search_plane(query: str) -> str:
    """Search planefyi.com for aircraft models, specs, engines, and manufacturers.

    Args:
        query: Search query string.
    """
    from planefyi.api import PlaneFYI

    with PlaneFYI() as api:
        data = api.search(query)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return f"No results found for \"{query}\"."
        items = results[:10] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
