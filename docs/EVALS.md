# Evals

Vibe Video ships a minimal eval harness that runs prompts against the
live Docker-hosted team and — when a case fails — writes a diagnostic
that Claude Code can read and act on to fix the prompt.

The whole system is five Python files (~480 LOC) plus one shell script.
Read them first if anything here is unclear: [evals/](../evals/).

## What it does

1. POSTs a prompt to `http://localhost:8000/teams/vibe_video/runs` with
   SSE streaming enabled.
2. Parses the stream into a `RunResult` (final content, tool calls,
   member responses, video paths, errors).
3. Asserts structured expectations from each `EvalCase`.
4. On **FAIL**, writes a markdown diagnostic to
   `evals/results/<case_id>.md`. The diagnostic contains:
   - the case spec and list of assertion failures
   - what the team actually did (response, tool calls, members, videos)
   - the last 200 lines of `docker compose logs vibe-video-api`
   - the full current contents of the instruction file for the target agent
   - a short instruction block telling Claude Code what to edit
5. [`scripts/eval_loop.sh`](../scripts/eval_loop.sh) loops: run → diagnose
   → `claude -p` edits the file → restart → retry, until pass or budget.

## Running the harness

Bring up the stack first:

```bash
docker compose up -d --build
```

Run all cases:

```bash
python -m evals run
```

Run one case:

```bash
python -m evals run --case greeting
```

Output is colorized PASS/FAIL/SKIPPED/ERROR per case. A timestamped JSON
summary is written to `evals/results/summary-<ts>.json` (gitignored).

### The autonomous loop

```bash
./scripts/eval_loop.sh dijkstra
```

Each iteration:
1. Runs the case. If PASS, exits 0.
2. Reads the diagnostic at `evals/results/dijkstra.md`.
3. Invokes `claude -p` with the diagnostic and a restricted tool
   allowlist (`Read,Edit,Grep,Glob` — no Bash, no Write of new files).
4. Checkpoints the edit as a git commit so every attempt is revertable
   (`git log | grep 'eval_loop: dijkstra'`).
5. Restarts `vibe-video-api` so the new instructions take effect.
6. Loops up to `MAX_ATTEMPTS` (default 5).

Environment overrides:

| Var            | Default                   |
|----------------|---------------------------|
| `MAX_ATTEMPTS` | 5                         |
| `BASE_URL`     | `http://localhost:8000`   |

## Case shape

Cases live in [evals/cases.py](../evals/cases.py). Each is a frozen
dataclass:

```python
EvalCase(
    id="dijkstra",
    prompt="Animate Dijkstra's algorithm on a small 5-node graph in a 20-second video.",
    expected_agent="animator",           # None = leader should answer directly
    response_contains=[],                # case-insensitive substrings
    expects_mp4=True,
    min_mp4_bytes=50_000,
    max_duration_s=600,
    target_file=_AGENTS / "animator.py", # which file `claude -p` edits on failure
    requires=[],                         # env vars; case is SKIPPED if missing
)
```

Add a case when a real regression surfaces. Resist the urge to split
cases into categories — one flat list is enough.

## Cost awareness

Each `run` invocation is a full team run, which means Anthropic API
spend. A case like `dijkstra` does a render (tens of tokens to minutes
of model time). The autonomous loop multiplies this by attempts × cases.

Start with one case at a time. `./scripts/eval_loop.sh <case>` is the
intended entry point, not the full suite.

## What's deliberately not in v1

- **No LLM judge.** Substring + MP4 + routing checks catch structural
  regressions. Add a judge when "did the video match the intent"
  becomes the bottleneck.
- **No cross-case regression check in the loop.** Fixing one case may
  break another; review `git diff` and rerun the full suite manually
  before committing.
- **No CI integration.** Evals cost real API dollars and rely on a live
  Docker container. Local-only for now.
- **No performance/latency tracking.** `max_duration_s` is a sanity
  bound, not a benchmark.
