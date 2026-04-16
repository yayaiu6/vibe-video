"""Eval cases — prompts with structured expectations.

Add a case when a real regression surfaces. Resist the urge to categorize.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_AGENTS = REPO_ROOT / "vibe_video" / "agents"
_TEAM = REPO_ROOT / "vibe_video" / "team.py"


@dataclass(frozen=True)
class EvalCase:
    id: str
    prompt: str
    # Which member should handle the request. None = leader answers directly.
    expected_agent: str | None = None
    # Substrings that MUST appear in the final response (case-insensitive).
    response_contains: list[str] = field(default_factory=list)
    # If True, at least one video must be produced and exist on disk.
    expects_mp4: bool = False
    min_mp4_bytes: int = 10_000
    max_duration_s: int = 300
    # Instruction file `run` will include in the diagnostic when this case fails.
    target_file: Path = _TEAM
    # Env vars that must be set; case is SKIPPED otherwise.
    requires: list[str] = field(default_factory=list)


CASES: list[EvalCase] = [
    EvalCase(
        id="greeting",
        prompt="hello",
        expected_agent=None,
        max_duration_s=60,
        target_file=_TEAM,
    ),
    EvalCase(
        id="dijkstra",
        prompt="Animate Dijkstra's algorithm on a small 5-node graph in a 20-second video.",
        expected_agent="animator",
        expects_mp4=True,
        min_mp4_bytes=50_000,
        max_duration_s=600,
        target_file=_AGENTS / "animator.py",
    ),
    EvalCase(
        id="repo_explore",
        prompt=("Clone github.com/agno-agi/agno and briefly explain what the Team class is for. Do not make a video."),
        expected_agent="code_explorer",
        response_contains=["Team"],
        max_duration_s=180,
        target_file=_AGENTS / "code_explorer.py",
    ),
    EvalCase(
        id="research",
        prompt="Briefly, what are the latest techniques for diffusion video models? No video, text only.",
        expected_agent="researcher",
        max_duration_s=180,
        target_file=_AGENTS / "researcher.py",
        requires=["PARALLEL_API_KEY"],
    ),
]


CASES_BY_ID: dict[str, EvalCase] = {c.id: c for c in CASES}


def get(case_id: str) -> EvalCase:
    if case_id not in CASES_BY_ID:
        raise KeyError(f"unknown case {case_id!r}; known: {sorted(CASES_BY_ID)}")
    return CASES_BY_ID[case_id]
