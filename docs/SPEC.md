# Vibe Video Specification

Vibe Video is a conversational multi-agent team that produces programmatic
motion-graphics videos using [Hyperframes](https://github.com/heygen-com/hyperframes)
(HeyGen's open-source HTML/GSAP render framework).

A user asks for a video. The team leader gathers context from one of three
sources — the model's own knowledge, the web (via Parallel), or an arbitrary
git repo — and hands a brief to the Animator specialist, who writes a
Hyperframes composition, renders it to MP4, and returns the clip.

This document is the canonical specification. All other docs derive from it.

---

## 1. Goals & Non-Goals

### Goals

- Deliver a working MP4 from a natural-language prompt, in one turn when
  the topic is in the model's knowledge, in a few turns when it needs
  research or codebase exploration.
- Keep the leader conversational and route all actual video work to a
  single specialist.
- Fit the "mini demo agent" family alongside
  [vibe-to-prd](https://github.com/agno-agi/vibe-to-prd): small footprint,
  one obvious thing it's for, clean defaults.

### Non-goals (explicit)

- No issue triage, PR review, or code contribution.
- No pre-configured repo list, no repo sync, no persistent on-disk repo
  cache beyond the session.
- No daily digest, no scheduled tasks.
- No Slack interface in v0. CLI + AgentOS web only.
- No Manim, no talking-head avatars, no TTS/voice cloning. Animator is
  Hyperframes-only. If we want a different renderer later, it's a
  separate spec.

---

## 2. Team Shape

```
VibeVideo (Team, Coordinate)
├── Researcher   (optional; requires PARALLEL_API_KEY)
├── CodeExplorer     (on-demand git clone + read-only code inspection)
└── Animator     (writes Hyperframes HTML, renders to MP4, iterates on failure)
```

- **Leader model**: Anthropic `claude-opus-4-7` via `agno.models.anthropic.Claude`.
- **Mode**: `TeamMode.coordinate` — leader delegates once per turn and
  synthesizes.
- **Leader tools**: none in v0 (no Slack, no direct render). Leader is
  pure conversation + routing.

### Routing rules

Respond directly only for:
- Greetings, thanks, "what can you do?"

Delegate everything else:
- **Researcher** — facts, docs, recent events, library/framework topics
  ("quantum entanglement", "how RAG works", "latest React hooks docs").
  Gated on `PARALLEL_API_KEY`; if absent, the leader tells the user and
  asks whether to proceed from model knowledge.
- **CodeExplorer** — anything that names a repo or points at specific code
  ("how does agno-agi/agno coordinate mode route a request"). Clones
  on demand; no pre-configured list.
- **Animator** — always the final delegate once enough context exists
  to write a brief. Receives: topic, key facts/structure to animate,
  desired length, style hints. Returns: rendered MP4 (as an
  `agno.media.Video`) and a short summary.

A single turn can chain: Researcher → Animator, or CodeExplorer → Animator,
or Researcher + CodeExplorer → Animator (rare; for "compare X in repo Y with
the algorithm in the paper").

---

## 3. Agents

### 3.1 Researcher

- **Tools**: `ParallelTools()`, `ReasoningTools()`.
- **Gating**: instantiated only when `PARALLEL_API_KEY` is set; `None`
  otherwise. Team constructs its member list filtering out `None`.
- **Responsibility**: return a compact, citeable brief (bullet facts +
  source URLs). Not prose essays. The Animator needs structured points,
  not paragraphs.

### 3.2 CodeExplorer

**No pre-configured repo list.** CodeExplorer owns an on-demand
`clone_repo(url)` tool and keeps clones in an ephemeral scratch dir
for the session.

- **Tools**:
  - `CodingTools` (read-only: `read_file`, `grep`, `find`, `ls`).
  - `GitTools` (trimmed — see §4.1): `clone_repo`, `git_log`, `git_diff`,
    `git_blame`, `git_show`, `git_branches`, `list_repos`, `repo_summary`.
  - `ReasoningTools()`.
- **No `GithubTools`**: PR/issue inspection isn't in Vibe Video's scope.
  If a user provides a repo URL with context like "this PR", CodeExplorer
  can read the PR branch via git, not via the GitHub API.
- **Scratch dir**: `REPOS_DIR` (default: `/repos` in Docker — an
  ephemeral named volume; `~/.cache/vibe-video/repos` locally).
  Session-scoped; nothing the user needs to inspect.
- **Responsibility**: clone, search, read, and return structured
  findings (file paths with line numbers, call chains, key snippets).

### 3.3 Animator

The specialist. Owns Hyperframes authoring end-to-end.

- **Tools**:
  - `HyperframesTools` (see §4.2): `render`, `lint`, `list_compositions`,
    `list_rendered_videos`.
  - `FileTools` (scoped to a per-session workspace dir): `save_file`,
    `read_file`, `list_files`. Needed so the agent can write
    `index.html`, compositions, and supporting assets before render.
  - `ReasoningTools()` — important, because iteration on render failures
    is where most of the cognitive work happens.
- **Instructions**: base prompt plus the **Hyperframes skill content**
  (see §5) inlined at agent-init time.
- **Workflow**:
  1. Receive brief (topic + key points + length + style hints).
  2. Plan scenes (use `think` for non-trivial briefs).
  3. Write `index.html` (+ per-scene compositions if needed) to a
     per-session workspace dir under `RENDERS_DIR`.
  4. Call `lint` (fast feedback). Fix issues.
  5. Call `render` with appropriate quality/fps. Default: quality=
     `standard`, fps=30, format=mp4.
  6. On failure: read stderr, fix the HTML/JS, retry up to `MAX_RENDER_RETRIES`
     (default 3). After the limit, surface the failure to the leader
     with a clear explanation.
  7. Return the rendered `Video` plus a one-paragraph summary of what
     was produced.
- **Model**: same `claude-opus-4-7` as the rest of the team.

---

## 4. Tools

### 4.1 `vibe_video/tools/git.py` — `GitTools`

Read-only git toolkit with an on-demand `clone_repo` helper. No
worktrees, no push — CodeExplorer is strictly read-only.

| Method | Purpose |
|---|---|
| `clone_repo(url, name?)` | Clone a public or PAT-authenticated repo into `base_dir`. Returns the local repo name. If already cloned, fast-forwards. |
| `list_repos()` | List currently cloned repos in `base_dir`. |
| `repo_summary(repo)` | Branch + top-level listing + README detection + recent commits. |
| `git_log`, `git_diff`, `git_blame`, `git_show`, `git_branches`, `get_github_remote` | Standard read-only git helpers. |

- All paths validated against `base_dir`.
- All subprocess calls timeout-bounded (30s default; 120s for pull,
  300s for initial clone).
- `GITHUB_ACCESS_TOKEN`, if set, is used by git's credential helper
  for HTTPS clones. Public repos clone without it.

### 4.2 `vibe_video/tools/hyperframes.py` — `HyperframesTools`

Thin Agno `Toolkit` wrapping the `hyperframes` CLI.

| Method | Purpose |
|---|---|
| `render(workspace, output_name?, fps?, quality?, format?, strict?)` | Renders the composition in `workspace` (a directory containing `index.html`) to MP4/WebM/MOV. Returns an `agno.media.Video`. On failure, returns the captured stderr so the agent can iterate. |
| `lint(workspace, strict?)` | Runs `hyperframes lint --json` and returns machine-readable validation results. |
| `list_compositions(workspace)` | Runs `hyperframes compositions` for discovery. |
| `list_rendered_videos(output_dir?)` | Lists rendered MP4s by mtime for the Animator's recall / follow-ups. |

Backed by the `hyperframes` npm package installed globally in the Docker
image. The toolkit invokes `npx hyperframes …` as a subprocess, captures
stderr on non-zero exits, and returns it verbatim so the agent can read
it. Timeouts default to 300s for `render`, 30s for `lint`.

Environment:
- `HYPERFRAMES_BIN` (optional) — explicit path to the CLI. Defaults to
  `npx hyperframes`.
- `PUPPETEER_EXECUTABLE_PATH` — passed through; lets us use a system
  Chromium instead of letting Puppeteer download one.
- `CONTAINER=true` — set in Docker.

---

## 5. Hyperframes Authoring Guide

Animator's system prompt embeds a compact, hand-written Hyperframes
authoring guide (~4 KB) directly in `vibe_video/agents/animator.py`.
It covers the composition shape, required `data-*` attributes, the
timeline contract, GSAP essentials, scene-transition rules, and the
hard don'ts — with one minimal working example.

**We intentionally do NOT pull in HeyGen's full 20 KB `SKILL.md`.**
That skill is authored for a standalone Claude Code agent running in
a filesystem with shell access, and it assumes conventions that don't
apply to our runtime:

- A "Visual Identity Gate" hard-rule that demands a `DESIGN.md` or
  `visual-style.md` before writing any HTML. We ship neither — Animator
  has a `Style defaults` section in its base prompt instead.
- Shell commands like `npx hyperframes validate` and
  `node skills/hyperframes/scripts/animation-map.mjs`. Animator has
  no shell — it has the `lint` and `render` tools.
- References to many sibling skill files (`house-style.md`,
  `references/captions.md`, etc.) that aren't part of our bundle.

Empirically, inlining the full skill caused the Animator to ignore its
tool-calling workflow and dump HTML into its reply text. The compact
inline guide avoids that.

If HeyGen publishes a future release we want to track, update the
inline skill in `animator.py` directly. No build-time fetch, no
external assets, no moving parts.

---

## 6. Rendering Pipeline

1. Leader delegates to Animator with a brief.
2. Animator plans and writes files to
   `RENDERS_DIR/<session_id>/<composition_name>/index.html`
   (plus optional `compositions/*.html`, assets, etc.).
3. Animator calls `HyperframesTools.render(workspace=...)`.
4. Toolkit shells to `npx hyperframes render <workspace> --output
   <out>.mp4 --fps 30 --quality standard --quiet`.
5. On success: toolkit loads the MP4 as an `agno.media.Video`, attaches
   it to the tool result. The team run response carries the video back
   through the leader to the interface (CLI prints path; AgentOS web
   plays inline).
6. On failure: toolkit returns captured stderr. Animator inspects,
   patches the HTML, retries. Up to `MAX_RENDER_RETRIES` times
   (default 3).
7. After the retry limit, Animator returns a structured failure:
   what it tried, what failed, and the last stderr.

---

## 7. Environment

### Required

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Leader + all agents. |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_DATABASE` | PostgreSQL + pgvector for session history and memory. |

### Optional

| Variable | Enables |
|---|---|
| `PARALLEL_API_KEY` | Researcher agent. Without it, Researcher is omitted from the team. |
| `GITHUB_ACCESS_TOKEN` | Cloning private repos via CodeExplorer. Public repos work without it. |
| `REPOS_DIR` | Override for the ephemeral clone scratch. Default `/repos` in Docker (named volume), `~/.cache/vibe-video/repos` locally. |
| `RENDERS_DIR` | Override for the render workspace + output root. Default `/renders` in Docker, `./renders` locally — both resolve to the same project-root `./renders/` directory because Docker bind-mounts it. |
| `MAX_RENDER_RETRIES` | Animator's render retry budget. Default `3`. |
| `HYPERFRAMES_BIN` | Override for `npx hyperframes`. |
| `JWT_VERIFICATION_KEY` | AgentOS auth in production. |

---

## 8. Interfaces

### CLI
`python -m vibe_video` — interactive REPL, streaming. Renders are written
to `RENDERS_DIR` and the path is printed in the final message.

### AgentOS web
`python -m app.main` (or `uvicorn app.main:app`). The AgentOS chat UI
plays the `Video` inline. This is the primary demo surface.

### No Slack (v0)
Slack support can be added later by re-introducing `SlackTools` + a
`Slack` interface, but MP4 delivery over Slack (upload API, 1 GB
bot-token limit, etc.) is a non-trivial addition and is deferred.

---

## 9. Memory & Persistence

- **Agentic memory** (team-level): captures user preferences like style,
  default length, aesthetic references ("3Blue1Brown-like"), narration
  preference. Mirrors the pattern used by `vibe-to-prd`.
- **Session history**: last 10 runs in-context; last 5 past sessions
  searchable.
- **No learnings KB**: Vibe Video has no "team conventions" to learn,
  so no vector store beyond what agentic memory uses.

---

## 10. Deployment

- Base image: a slim Debian + Python 3.12 + Node 22 + FFmpeg + Chromium.
  Puppeteer is told to use the system Chromium via
  `PUPPETEER_EXECUTABLE_PATH` to avoid the 150 MB download.
- `hyperframes` is installed globally via `npm install -g hyperframes`
  during image build.
- The Hyperframes authoring guide is inlined directly in
  `vibe_video/agents/animator.py` — no build-time fetch, no external
  skill assets (see §5).
- PostgreSQL + pgvector runs as a sidecar service via `compose.yaml`.
- Volumes:
  - `./renders` — **bind-mounted** from the project root so finished
    MP4s appear right in the checkout (gitignored).
  - `repos` — named Docker volume, ephemeral scratch for CodeExplorer.
  - `pgdata` — named Docker volume for PostgreSQL.

---

## 11. Scheduled Tasks

Vibe Video ships **no pre-registered schedules**. It has no background
work of its own — no repo sync, no daily digest, no triage.

The AgentOS scheduler is, however, **enabled** (`scheduler=True` in
`app/main.py`). The web UI exposes its scheduling surface so users can
set up their own recurring runs against the team or any agent — e.g. a
weekly "render the top 3 commits from `agno-agi/agno`" job, or a daily
brief that hands the Researcher → Animator chain to a fixed topic.
Schedules live in Postgres via `agno.scheduler.ScheduleManager` and
survive restarts. Base URL is set via `AGENTOS_URL` (default
`http://127.0.0.1:8000`).

---

## 12. Example Prompts

A representative set of things Vibe Video should handle well.

**Pure Animator** (no research, no exploration):
- "Animate Dijkstra's algorithm on a small weighted graph."
- "Show a Fourier series building up a square wave."
- "Animate a red-black tree insertion with a rotation."
- "Animate gradient descent on a 2D loss surface."

**Researcher → Animator**:
- "Make a 45-second video explaining quantum entanglement."
- "Explain the CAP theorem with a worked partition example."
- "Animate how RSA works with toy numbers."

**CodeExplorer → Animator**:
- "Clone agno-agi/agno and animate how `Team.coordinate` routes a request."
- "In facebook/react, animate the reconciler's commit phase at a high level."

**Iteration**:
- (Follow-up) "Too fast. Slow scene 2 down and add a caption."

**Graceful degradation**:
- `PARALLEL_API_KEY` unset + "explain quantum entanglement" → leader
  explains research is unavailable, offers model-knowledge fallback.
- Extremely large clone target → CodeExplorer surfaces a clean timeout
  rather than hanging.

---

## 13. Evals

A minimal harness lives under `evals/` and is driven by
`python -m evals run`. It POSTs prompts to the live team via
`/teams/vibe_video/runs`, parses the SSE stream, and asserts structured
expectations (expected routing, substring matches, MP4 existence + size,
run-level errors, duration bound).

On **FAIL**, a markdown diagnostic is written to
`evals/results/<case_id>.md` containing: the case spec, what the team
actually did, the last 200 lines of container logs, and the full current
contents of the target instruction file. `scripts/eval_loop.sh` feeds
that diagnostic to `claude -p` (headless, restricted tool allowlist) so
Claude Code can edit the instruction file and the harness can retry —
no human in the loop beyond the initial `./scripts/eval_loop.sh <case>`
invocation and a final `git diff` review.

Cases are defined in `evals/cases.py` as `EvalCase` dataclasses. Each
case names the instruction file it is testing; that is the file
Claude Code edits when the case fails. No LLM judge in v1 — substring +
MP4 + routing checks are sufficient for structural regressions.

See [docs/EVALS.md](EVALS.md) for usage, and [evals/](../evals/) for
the (~480 LOC) implementation.

---

## 14. Open Questions (explicit)

Tracked as `TODO(spec)` where relevant in code. Resolve before v1.

- **Asset pipeline**: how does Animator handle briefs that need
  external images (logos, photos)? v0 punt: model-written SVGs only;
  no external asset fetch.
- **Audio**: Hyperframes supports audio tracks via `<audio>`. v0 punt:
  no audio. Follow-up adds the Hyperframes `tts` CLI command as a
  tool.
- **Render workers**: `hyperframes render --workers N` speeds up
  multi-scene renders. v0 uses `auto`.
- **Skill pinning**: do we want to ship a vendored copy of the
  skills in-repo rather than fetching at build? Tradeoff between
  reproducibility and freshness.
