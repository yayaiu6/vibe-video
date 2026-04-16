"""Hyperframes toolkit.

Thin wrapper around the `hyperframes` CLI. The Animator agent uses this
to lint and render HTML compositions to MP4, iterating on failures.

The CLI operates on a project *directory* (which must contain an
`index.html`), not a single file. Animator is responsible for writing
the workspace; this toolkit only drives the CLI.

CLI reference: https://github.com/heygen-com/hyperframes
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Literal

from agno.media import Video
from agno.tools import Toolkit
from agno.tools.function import ToolResult
from agno.utils.log import logger

Quality = Literal["draft", "standard", "high"]
Format = Literal["mp4", "webm", "mov"]

# ---------------------------------------------------------------------------
# Defaults (env-overridable)
# ---------------------------------------------------------------------------
_DEFAULT_BIN = os.environ.get("HYPERFRAMES_BIN", "npx hyperframes")
_DEFAULT_RENDER_TIMEOUT = int(os.environ.get("HYPERFRAMES_RENDER_TIMEOUT", "300"))
_DEFAULT_LINT_TIMEOUT = int(os.environ.get("HYPERFRAMES_LINT_TIMEOUT", "30"))

# Truncate captured stderr we pass back to the agent so a runaway error
# doesn't blow out the context window.
_STDERR_LIMIT = 8000


class HyperframesTools(Toolkit):
    """Agno toolkit wrapping the Hyperframes CLI."""

    def __init__(
        self,
        base_dir: str,
        bin_command: str = _DEFAULT_BIN,
        render_timeout: int = _DEFAULT_RENDER_TIMEOUT,
        lint_timeout: int = _DEFAULT_LINT_TIMEOUT,
    ):
        super().__init__(
            name="hyperframes_tools",
            tools=[
                self.render,
                self.lint,
                self.list_compositions,
                self.list_rendered_videos,
            ],
        )
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        # `bin_command` may contain flags ("npx hyperframes"), so we split it.
        self._bin_argv = shlex.split(bin_command)
        self.render_timeout = render_timeout
        self.lint_timeout = lint_timeout

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _workspace_path(self, workspace: str) -> Path:
        """Resolve a workspace name to an absolute path under base_dir.

        The workspace is the directory containing `index.html`.
        """
        resolved = (self.base_dir / workspace).resolve()
        if not resolved.is_relative_to(self.base_dir):
            raise ValueError(f"Workspace escapes base directory: {workspace}")
        return resolved

    def _run(self, argv: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
        """Run the CLI with standard settings."""
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env={**os.environ, "CONTAINER": os.environ.get("CONTAINER", "true")},
        )

    @staticmethod
    def _truncate(text: str) -> str:
        if len(text) <= _STDERR_LIMIT:
            return text
        return text[:_STDERR_LIMIT] + f"\n... [truncated — exceeded {_STDERR_LIMIT} chars]"

    @staticmethod
    def _safe_output_name(name: str) -> str:
        """Normalize an output filename to a safe single-segment name."""
        base = Path(name).name or "video"
        base = re.sub(r"[^A-Za-z0-9._-]", "_", base)
        return base or "video"

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------

    def render(
        self,
        workspace: str,
        output_name: str = "video.mp4",
        fps: int = 30,
        quality: Quality = "standard",
        format: Format = "mp4",
        strict: bool = False,
    ) -> ToolResult:
        """Render a Hyperframes composition to a video file.

        The `workspace` must be a directory under the tool's base_dir that
        contains an `index.html`. On success, returns a `ToolResult` whose
        `videos=[Video(...)]` attaches the rendered MP4 to the run. On
        failure, returns a `ToolResult` with the captured stderr in
        `content` so the agent can read it and iterate.

        Args:
            workspace: Directory name under base_dir that holds `index.html`.
            output_name: Output filename (written alongside the workspace).
                Non-alphanumeric characters (except `._-`) are replaced.
            fps: Frames per second (default 30).
            quality: 'draft', 'standard' (default), or 'high'.
            format: 'mp4' (default), 'webm', or 'mov'.
            strict: If True, passes `--strict-all` to fail on any warnings.
        """
        try:
            ws = self._workspace_path(workspace)
            if not (ws / "index.html").is_file():
                return ToolResult(content=f"Error: workspace '{workspace}' is missing index.html")

            out_name = self._safe_output_name(output_name)
            out_path = ws / out_name

            argv = [
                *self._bin_argv,
                "render",
                ".",
                "--output",
                str(out_path),
                "--fps",
                str(fps),
                "--quality",
                quality,
                "--format",
                format,
                "--quiet",
            ]
            if strict:
                argv.append("--strict-all")

            result = self._run(argv, cwd=ws, timeout=self.render_timeout)
            if result.returncode != 0 or not out_path.is_file():
                stderr = self._truncate(result.stderr or result.stdout or "(no output)")
                return ToolResult(
                    content=(
                        f"Error: render failed (exit {result.returncode}).\n"
                        f"Inspect the error below, patch index.html, and retry.\n\n"
                        f"--- stderr ---\n{stderr}"
                    )
                )

            # Read the bytes into memory and attach via Video(content=...).
            # Agno base64-inlines content at serialization time so the web UI
            # receives a self-contained blob it can <video> — a filepath ref
            # does not propagate. Tradeoff: the SSE payload carries the MP4
            # (~1 MB for a 45s composition at standard quality; inflates to
            # ~1.3 MB base64'd). Fine at our target lengths; trim quality or
            # duration if the event stream starts choking on multi-MB payloads.
            # Pattern from agno-agi/agno#7554 (Manim toolkit).
            mime = {"mp4": "video/mp4", "webm": "video/webm", "mov": "video/quicktime"}[format]
            mp4_bytes = out_path.read_bytes()
            video = Video(content=mp4_bytes, format=format, mime_type=mime)
            size_kb = len(mp4_bytes) // 1024
            return ToolResult(
                content=(f"Rendered successfully to {out_path} ({size_kb} KB, {fps} fps, quality={quality})."),
                videos=[video],
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                content=(
                    f"Error: render timed out after {self.render_timeout}s. "
                    f"Consider a lower quality ('draft') or a shorter composition."
                )
            )
        except Exception as e:
            logger.warning(f"render failed: {e}")
            return ToolResult(content=f"Error: {e}")

    def lint(self, workspace: str, strict: bool = False) -> str:
        """Validate a Hyperframes workspace before rendering.

        Much faster than `render` — use this first after edits.

        Args:
            workspace: Directory name under base_dir that holds `index.html`.
            strict: If True, passes `--strict` to surface warnings as errors.

        Returns:
            The lint output (JSON-formatted if supported, otherwise raw).
        """
        try:
            ws = self._workspace_path(workspace)
            argv = [*self._bin_argv, "lint", ".", "--json"]
            if strict:
                argv.append("--strict")
            result = self._run(argv, cwd=ws, timeout=self.lint_timeout)
            output = result.stdout.strip() or result.stderr.strip() or "(no output)"
            # If lint returned JSON, pretty-print so the agent reads it cleanly.
            try:
                parsed = json.loads(output)
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                return self._truncate(output)
        except subprocess.TimeoutExpired:
            return f"Error: lint timed out after {self.lint_timeout}s"
        except Exception as e:
            logger.warning(f"lint failed: {e}")
            return f"Error: {e}"

    def list_compositions(self, workspace: str) -> str:
        """List compositions discovered in a workspace.

        Wraps `hyperframes compositions`. Useful for multi-scene projects.
        """
        try:
            ws = self._workspace_path(workspace)
            argv = [*self._bin_argv, "compositions"]
            result = self._run(argv, cwd=ws, timeout=self.lint_timeout)
            return self._truncate(result.stdout.strip() or result.stderr.strip() or "(no output)")
        except Exception as e:
            logger.warning(f"list_compositions failed: {e}")
            return f"Error: {e}"

    def list_rendered_videos(self, output_dir: str = "") -> str:
        """List previously rendered video files under base_dir.

        Args:
            output_dir: Optional subdirectory to scope the listing.
                Defaults to scanning all workspaces.

        Returns:
            Newline-separated list of `<relative path>\\t<size>\\t<mtime>`.
        """
        try:
            root = self._workspace_path(output_dir) if output_dir else self.base_dir
            if not root.is_dir():
                return "(directory not found)"
            rows: list[tuple[float, str]] = []
            for ext in ("*.mp4", "*.webm", "*.mov"):
                for p in root.rglob(ext):
                    try:
                        st = p.stat()
                    except OSError:
                        continue
                    rel = p.relative_to(self.base_dir)
                    rows.append((st.st_mtime, f"{rel}\t{st.st_size}\t{int(st.st_mtime)}"))
            if not rows:
                return "(no rendered videos yet)"
            rows.sort(reverse=True)
            return "\n".join(row for _, row in rows[:50])
        except Exception as e:
            logger.warning(f"list_rendered_videos failed: {e}")
            return f"Error: {e}"
