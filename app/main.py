"""
Vibe Video AgentOS
==================

The main entry point for Vibe Video.

Run:
    python -m app.main
"""

import mimetypes
from os import getenv
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, Response

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
RENDERS_DIR = Path(getenv("RENDERS_DIR", "/app/renders"))
# Also check /app/renders as the Animator agent writes there
RENDERS_DIR_ALT = Path("/app/renders")

# Pre-compute which frontend pages exist so we don't hit disk on every request.
_FRONTEND_PAGES: dict[str, Path] = {}
if FRONTEND_DIR.is_dir():
    for _name in ("index.html", "create.html", "history.html", "settings.html"):
        _p = FRONTEND_DIR / _name
        if _p.is_file():
            _FRONTEND_PAGES["/" + _name if _name != "index.html" else "/"] = _p

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
# Frontend middleware — intercepts requests *before* AgentOS routes.
# Serves static CSS/JS/assets and HTML pages from the frontend/ directory.
# ---------------------------------------------------------------------------
class FrontendMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # --- Rendered videos: /renders/* ---
        if path.startswith("/renders/"):
            rel = path[len("/renders/"):]
            # Check both RENDERS_DIR and /app/renders (Animator writes there)
            for render_dir in (RENDERS_DIR, RENDERS_DIR_ALT):
                file_path = render_dir / rel
                if file_path.is_file():
                    return FileResponse(str(file_path), media_type="video/mp4")

        # --- Static files: /css/*, /js/*, /assets/* ---
        if path.startswith(("/css/", "/js/", "/assets/")):
            file_path = FRONTEND_DIR / path.lstrip("/")
            if file_path.is_file():
                media_type, _ = mimetypes.guess_type(file_path.name)
                return FileResponse(str(file_path), media_type=media_type)

        # --- HTML pages: /, /create.html, /history.html, /settings.html ---
        if path in _FRONTEND_PAGES:
            return FileResponse(str(_FRONTEND_PAGES[path]))

        # --- Everything else falls through to AgentOS ---
        return await call_next(request)


app.add_middleware(FrontendMiddleware)


if __name__ == "__main__":
    agent_os.serve(
        app="app.main:app",
        reload=runtime_env == "dev",
    )
