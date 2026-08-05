"""
Vibe Video AgentOS
==================

The main entry point for Vibe Video.

Run:
    python -m app.main
"""

from os import getenv
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# ---------------------------------------------------------------------------
# Create AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    name="Vibe Video",
    tracing=True,
    scheduler=True,
    scheduler_base_url=scheduler_base_url,
    db=get_postgres_db(),
    teams=[vibe_video],
    agents=[a for a in [code_explorer, researcher, animator] if a is not None],
    config=str(Path(__file__).parent / "config.yaml"),
    authorization=runtime_env == "prd",
)

app = agent_os.get_app()

# ---------------------------------------------------------------------------
# Mount frontend static files
# ---------------------------------------------------------------------------
_css = FRONTEND_DIR / "css"
_js = FRONTEND_DIR / "js"
_assets = FRONTEND_DIR / "assets"

if _css.is_dir():
    app.mount("/css", StaticFiles(directory=str(_css)), name="css")
if _js.is_dir():
    app.mount("/js", StaticFiles(directory=str(_js)), name="js")
if _assets.is_dir():
    app.mount("/assets", StaticFiles(directory=str(_assets)), name="assets")

if FRONTEND_DIR.is_dir():
    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    @app.get("/create.html", include_in_schema=False)
    async def serve_create():
        return FileResponse(str(FRONTEND_DIR / "create.html"))

    @app.get("/history.html", include_in_schema=False)
    async def serve_history():
        return FileResponse(str(FRONTEND_DIR / "history.html"))

    @app.get("/settings.html", include_in_schema=False)
    async def serve_settings():
        return FileResponse(str(FRONTEND_DIR / "settings.html"))


if __name__ == "__main__":
    agent_os.serve(
        app="app.main:app",
        reload=runtime_env == "dev",
    )
