import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)

WORKSPACE_ROOT = Path("/Users/federicofailla/devs/projects")
HUB_DIR = WORKSPACE_ROOT / "project-hub"

DOCKER_MODEL_RUNNER_URL = "http://localhost:12434/engines/llama.cpp/v1"
DOCKER_MODEL_NAME = "ai/gemma3"

# Each project: optional dev port (None = no local server), human-readable stack
KNOWN_PROJECTS: dict[str, dict] = {
    "wealthtrack": {
        "port": 3000,
        "stack": "Next.js, React 19, Tailwind CSS 4, Prisma",
        "status": "Active",
    },
    "investracker": {
        "port": 8080,
        "stack": "Java 11, Spring Boot 2.7, PostgreSQL",
        "status": "Stable",
    },
    "importer-porfolio": {
        "port": 3000,
        "stack": "React 18, Redux Toolkit, MUI 5",
        "status": "Stable",
    },
    "cv-generator": {
        "port": 5173,
        "stack": "Vite, React 18, TypeScript, Tailwind CSS",
        "status": "Stable",
    },
    "healthVault": {
        "port": None,
        "stack": "Markdown, CSV, Python (planned)",
        "status": "In Dev",
    },
    "agents": {
        "port": None,
        "stack": "Python 3.12, OpenAI Agents SDK, LangGraph, CrewAI, AutoGen",
        "status": "Research",
    },
    "java-servlets": {
        "port": None,
        "stack": "Java (legacy)",
        "status": "Legacy",
    },
}

_docker_client: AsyncOpenAI | None = None
_docker_available: bool = False


async def init_model_clients() -> None:
    """Probe Docker Model Runner once at startup. Gracefully sets fallback if unreachable."""
    global _docker_client, _docker_available
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{DOCKER_MODEL_RUNNER_URL}/models",
                headers={"Authorization": "Bearer docker"},
                timeout=3.0,
            )
            if resp.status_code == 200:
                models = resp.json().get("data", [])
                if models:
                    _docker_client = AsyncOpenAI(
                        base_url=DOCKER_MODEL_RUNNER_URL,
                        api_key="docker",
                    )
                    _docker_available = True
                    print(f"[hub] Docker Model Runner online — using {DOCKER_MODEL_NAME}")
                    return
    except Exception:
        pass
    print("[hub] Docker Model Runner unavailable — all tiers will use gpt-4o-mini")


def get_model(tier: str = "fast"):
    """
    When Docker Model Runner is available, ALL tiers use the local model (zero cost).
    When Docker is unavailable, falls back to OpenAI (requires OPENAI_API_KEY):
      tier='fast'  → gpt-4o-mini
      tier='smart' → gpt-4o-mini (or HUB_SMART_MODEL env var override)
    """
    if _docker_available and _docker_client is not None:
        from agents import OpenAIChatCompletionsModel

        return OpenAIChatCompletionsModel(
            model=DOCKER_MODEL_NAME,
            openai_client=_docker_client,
        )

    smart_model = os.getenv("HUB_SMART_MODEL", "gpt-4o-mini")
    return smart_model
