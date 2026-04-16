# Vibe Video

A multi-agent team that makes short motion-graphics videos from natural-language.

Ask for a video and Vibe Video gathers what it needs — from the model's own knowledge, from the web, or from an arbitrary git repo — then hands the brief to an Animator specialist that writes a [Hyperframes](https://github.com/heygen-com/hyperframes) HTML composition and renders it to MP4.

## How It Works

```
Vibe Video (Team Leader Coordinates)
├── Animator        — writes Hyperframes HTML, renders to MP4, iterates on failure
├── CodeExplorer    — clones any git repo on demand, read-only
└── Researcher      — Parallel web search (optional; set PARALLEL_API_KEY)
```

The team leader routes requests to one of the specialists and synthesizes the result. The Animator owns the full authoring loop: planning scenes, writing HTML + GSAP, linting, rendering, and iterating when the render fails.

The product specification is documented in [`docs/SPEC.md`](docs/SPEC.md).

## Example Prompts

**Pure Animator** (model knowledge is enough):
- "Animate Dijkstra's algorithm on a small weighted graph."
- "Show a Fourier series building up a square wave."
- "Animate gradient descent on a 2D loss surface."

**Researcher → Animator** (needs web research):
- "Make a 45-second video explaining quantum entanglement."
- "Explain the CAP theorem with a worked partition example."

**CodeExplorer → Animator** (needs to read real code):
- "Clone agno-agi/agno and animate how `Team.coordinate` routes a request."
- "In facebook/react, animate the reconciler's commit phase at a high level."

**Follow-ups**:
- "Too fast. Slow scene 2 down and add a caption."
- "Re-render with quality='high'."

## Get Started

### 1. Clone and configure

```bash
git clone https://github.com/agno-agi/vibe-video.git
cd vibe-video
cp example.env .env
```

Edit `.env`:
- `ANTHROPIC_API_KEY` — required (we use `claude-opus-4-7`)
- `PARALLEL_API_KEY` — optional, enables web research
- `GITHUB_ACCESS_TOKEN` — optional, enables cloning private repos

### 2. Run with Docker

```bash
docker compose up -d --build
```

The first build takes a few minutes because it installs Node 22, FFmpeg, Chromium, and the `hyperframes` CLI into the image.

### 3. Use it

1. Open the AgentOS web UI at [https://os.agno.com/](https://os.agno.com/)
2. Add **https://localhost:8000** as an OS.
3. Chat with the team. MP4s play inline.

### 4. Rendered videos

Outputs land in `./renders/` at the project root — bind-mounted into the container so finished MP4s are immediately accessible on the host. Each composition gets its own subdirectory containing the authored HTML and the final MP4. The directory is gitignored.

## Local Development

```bash
./scripts/venv_setup.sh && source .venv/bin/activate
docker compose up -d vibe-video-db    # Just the database
python -m vibe_video                  # CLI REPL
```

Local rendering requires Node 22, FFmpeg, and a Chromium binary on PATH:

```bash
# macOS
brew install node ffmpeg chromium
npm install -g hyperframes

# Linux (Debian/Ubuntu)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt install -y nodejs ffmpeg chromium
sudo npm install -g hyperframes
```

## Architecture at a Glance

See [`docs/SPEC.md`](docs/SPEC.md) for the full specification — team structure, agent responsibilities, tool surface, rendering pipeline, environment variables, and the v0 non-goals.

Source layout:

```
vibe_video/
├── team.py                # Leader + routing
├── agents/
│   ├── animator.py        # Hyperframes HTML → MP4 (inlines compact skill)
│   ├── code_explorer.py   # On-demand git clone + read
│   └── researcher.py      # Parallel web search (optional)
├── tools/
│   ├── git.py             # clone_repo + read-only git
│   └── hyperframes.py     # CLI wrapper: render, lint, list
└── settings.py            # DB, paths, model, retry budget
```

## Evals

A minimal harness runs prompts against the live Docker team and auto-fixes prompt regressions with `claude -p` in a loop.

```bash
python -m evals run                      # run all cases
python -m evals run --case dijkstra      # run one case
./scripts/eval_loop.sh dijkstra          # autonomous fix loop
```

See [`docs/EVALS.md`](docs/EVALS.md) for the full workflow.

## License

Apache-2.0. See [LICENSE](LICENSE).
