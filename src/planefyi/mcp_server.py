"""MCP server for planefyi."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from planefyi.api import PlaneFYI

mcp = FastMCP("planefyi")


@mcp.tool()
def search_planefyi(query: str) -> dict[str, Any]:
    """Search planefyi.com for content matching the query."""
    with PlaneFYI() as api:
        return api.search(query)
