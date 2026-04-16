"""
Vibe Video AgentOS
==================

The main entry point for Vibe Video.

Run:
    python -m app.main
"""

from os import getenv
from pathlib import Path

from agno.os import AgentOS

from db import get_postgres_db
from vibe_video.agents.animator import animator
from vibe_video.agents.code_explorer import code_explorer
from vibe_video.agents.researcher import researcher
from vibe_video.team import vibe_video

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
runtime_env = getenv("RUNTIME_ENV", "prd")
scheduler_base_url = getenv("AGENTOS_URL", "http://127.0.0.1:8000")

# ---------------------------------------------------------------------------
# Create AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    name="Vibe Video",
    tracing=True,
    # Vibe Video has no scheduled jobs of its own, but enabling the
    # scheduler surfaces AgentOS's scheduling UI so users can set up
    # their own recurring runs (e.g. a weekly "render last week's
    # commits" job).
    scheduler=True,
    scheduler_base_url=scheduler_base_url,
    db=get_postgres_db(),
    teams=[vibe_video],
    agents=[a for a in [code_explorer, researcher, animator] if a is not None],
    config=str(Path(__file__).parent / "config.yaml"),
    authorization=runtime_env == "prd",
)

app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(
        app="app.main:app",
        reload=runtime_env == "dev",
    )
