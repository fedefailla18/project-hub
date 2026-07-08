"""
Gradio web UI for the Project Hub Orchestrator.

Launch via: uv run hub ui  (or: uv run python src/hub/ui/app.py)
"""

import asyncio

import gradio as gr

_initialized = False


async def _ensure_initialized() -> None:
    global _initialized
    if not _initialized:
        from hub.config import init_model_clients

        await init_model_clients()
        _initialized = True


async def chat(message: str, history: list) -> str:
    await _ensure_initialized()
    from hub.agents.orchestrator import run_orchestrator

    return await run_orchestrator(message)


def launch_ui() -> None:
    with gr.Blocks(
        title="Project Hub Orchestrator",
        theme=gr.themes.Default(primary_hue="sky"),
    ) as ui:
        gr.Markdown(
            "# Project Hub — Workspace Orchestrator\n"
            "Ask about any project in your workspace. "
            "The orchestrator reads live git state, not stale notes."
        )

        gr.ChatInterface(
            fn=chat,
            type="messages",
            examples=[
                "What is the state of wealthtrack?",
                "Which projects have uncommitted changes?",
                "Give me a full workspace health report",
                "What should I work on today?",
                "Update my task board based on current project states",
                "Show me the last 5 commits in investracker",
            ],
        )

    ui.launch(inbrowser=True)


if __name__ == "__main__":
    launch_ui()
