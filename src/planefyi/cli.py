"""Command-line interface for planefyi."""

from __future__ import annotations

import json

import typer

from planefyi.api import PlaneFYI

app = typer.Typer(help="PlaneFYI — Aircraft models and specifications API client.")


@app.command()
def search(query: str) -> None:
    """Search planefyi.com."""
    with PlaneFYI() as api:
        result = api.search(query)
        typer.echo(json.dumps(result, indent=2))
