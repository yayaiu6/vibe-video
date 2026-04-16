# ===========================================================================
# Vibe Video — multi-agent team that renders Hyperframes videos
# ===========================================================================

FROM agnohq/python:3.12

# Pinned by default for reproducible builds; override at build time with
#   docker build --build-arg HYPERFRAMES_VERSION=x.y.z ...
ARG HYPERFRAMES_VERSION=0.3.2

# ---------------------------------------------------------------------------
# Puppeteer: use the system Chromium rather than the ~170 MB download.
# Set BEFORE `npm install -g hyperframes` so the postinstall sees it.
# ---------------------------------------------------------------------------
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    CONTAINER=true

# ---------------------------------------------------------------------------
# System dependencies
# ---------------------------------------------------------------------------
# - git: CodeExplorer clones repos on demand.
# - ffmpeg: Hyperframes' render pipeline invokes ffmpeg to stitch frames.
# - chromium + fonts: Puppeteer renders compositions in a headless browser.
# - curl + ca-certificates + gnupg: used by the NodeSource setup script.
# ---------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    openssh-client \
    curl \
    ca-certificates \
    gnupg \
    ffmpeg \
    chromium \
    fonts-liberation \
    fonts-noto \
    fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Node.js 22 (required by Hyperframes) + pinned hyperframes CLI
# ---------------------------------------------------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g "hyperframes@${HYPERFRAMES_VERSION}" \
    && npm cache clean --force

# ---------------------------------------------------------------------------
# Git configuration (safe defaults for agent use)
# ---------------------------------------------------------------------------
RUN git config --system init.defaultBranch main \
    && git config --system user.name "Vibe Video" \
    && git config --system user.email "vibe-video@localhost" \
    && git config --system advice.detachedHead false \
    && git config --system --add safe.directory '*'

# ---------------------------------------------------------------------------
# GitHub token credential helper (for CodeExplorer cloning private repos)
# ---------------------------------------------------------------------------
# GITHUB_ACCESS_TOKEN env var is consumed at runtime. The helper reads it
# from memory and feeds it to git over stdin — never written to disk.
# Placed here (above COPY . .) so it's cached independently of app code.
# ---------------------------------------------------------------------------
RUN printf '%s\n' \
        '#!/bin/bash' \
        'if [ -n "$GITHUB_ACCESS_TOKEN" ]; then' \
        '    echo "protocol=https"' \
        '    echo "host=github.com"' \
        '    echo "username=x-access-token"' \
        '    echo "password=$GITHUB_ACCESS_TOKEN"' \
        'fi' \
        > /usr/local/bin/git-credential-vibe-video \
    && chmod +x /usr/local/bin/git-credential-vibe-video \
    && git config --system credential.helper '/usr/local/bin/git-credential-vibe-video'

# ---------------------------------------------------------------------------
# Runtime directories
# ---------------------------------------------------------------------------
RUN mkdir -p /repos /renders

# ---------------------------------------------------------------------------
# Python dependencies
# ---------------------------------------------------------------------------
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --no-cache-dir --system -r requirements.txt

# ---------------------------------------------------------------------------
# Application code
# ---------------------------------------------------------------------------
COPY . .
ENV PYTHONPATH=/app

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
RUN chmod +x /app/scripts/entrypoint.sh
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# ---------------------------------------------------------------------------
# Default command (overridden by compose)
# ---------------------------------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
