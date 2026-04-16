"""
Shared settings for Vibe Video.

Centralizes the database, scratch directories, and model choice
so every agent pulls from the same sources.
"""

from os import getenv
from pathlib import Path

from agno.models.anthropic import Claude

from db import get_postgres_db

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
agent_db = get_postgres_db()

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
# Anthropic Claude Opus 4.7 — strong reasoning, great for multi-step
# planning and Hyperframes HTML authoring.
MODEL = Claude(id="claude-opus-4-7")

# Animator writes whole HTML compositions inside `save_file` tool calls,
# so its output is several thousand tokens of HTML + CSS + GSAP.
#
# Extended thinking is DISABLED here. Empirically, even with
# `thinking={"type": "adaptive"}` + `output_config={"effort": "medium"}`,
# Opus 4.7 burns the entire output budget on thinking before emitting a
# single tool call (observed: output=16000, time_to_first_token = full
# duration, zero tool calls). Disabling thinking routes the full budget
# to actual output — the HTML and tool calls we need.
#
# max_tokens is set high so one `save_file` call can carry a full
# composition (HTML + inline CSS + GSAP is ~6-10k tokens for a busy
# animation).
ANIMATOR_MODEL = Claude(
    id="claude-opus-4-7",
    max_tokens=32000,
)

# ---------------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------------
_LOCAL_CACHE = Path.home() / ".cache" / "vibe-video"
_PROJECT_ROOT = Path(__file__).parent.parent

# REPOS_DIR — scratch for CodeExplorer's on-demand clones. Session-scoped
# and not something the user needs to inspect, so it lives outside the
# project tree by default. In Docker this is overridden to /repos
# (an ephemeral named volume).
REPOS_DIR = Path(getenv("REPOS_DIR", str(_LOCAL_CACHE / "repos")))
REPOS_DIR.mkdir(parents=True, exist_ok=True)

# RENDERS_DIR — MP4 outputs and per-composition HTML workspaces. Lives in
# the project root so the developer can open finished videos directly
# from the tree (gitignored). In Docker this is bind-mounted to ./renders.
RENDERS_DIR = Path(getenv("RENDERS_DIR", str(_PROJECT_ROOT / "renders")))
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Animator behavior
# ---------------------------------------------------------------------------
MAX_RENDER_RETRIES = int(getenv("MAX_RENDER_RETRIES", "3"))
