"""
CLI entry point for project-hub.

Usage (after uv sync):
    uv run hub scan
    uv run hub ask "what is the state of wealthtrack?"
    uv run hub update
    uv run hub ui
"""

import asyncio

import click
from rich.console import Console
from rich.markdown import Markdown

console = Console()

_initialized = False


async def _ensure_initialized() -> None:
    global _initialized
    if not _initialized:
        from hub.config import init_model_clients

        await init_model_clients()
        _initialized = True


async def _run(message: str) -> str:
    await _ensure_initialized()
    from hub.agents.orchestrator import run_orchestrator

    return await run_orchestrator(message)


@click.group()
def cli() -> None:
    """Project Hub — AI orchestration service for your dev workspace."""


@cli.command()
@click.argument("question")
def ask(question: str) -> None:
    """Ask the orchestrator a question about any project.

    \b
    Examples:
        hub ask "what is the state of wealthtrack?"
        hub ask "which projects have uncommitted changes?"
        hub ask "what should I work on today?"
    """
    result = asyncio.run(_run(question))
    console.print(Markdown(result))


@cli.command()
def scan() -> None:
    """Scan all projects and print a workspace health report."""
    result = asyncio.run(
        _run(
            "Call get_full_workspace_scan and give me a health report for every project. "
            "For each project include: health score, last commit message and age, "
            "uncommitted changes (if any), and dev server status. Format as a markdown table "
            "followed by a short summary of what needs attention."
        )
    )
    console.print(Markdown(result))


@cli.command()
def update() -> None:
    """Scan all projects and rewrite active_tasks.md + inventory.md."""
    console.print("[dim]Scanning all projects and updating task board...[/dim]")
    result = asyncio.run(
        _run(
            "Use update_task_board to scan all projects and update active_tasks.md and "
            "inventory.md based on current health. Then summarize what was changed."
        )
    )
    console.print(Markdown(result))


@cli.command()
def ui() -> None:
    """Launch the Gradio web UI at http://localhost:7860."""
    from hub.ui.app import launch_ui

    launch_ui()


if __name__ == "__main__":
    cli()
