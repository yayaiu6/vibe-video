"""CLI entry point: python -m vibe_video"""

from vibe_video.team import vibe_video

if __name__ == "__main__":
    vibe_video.cli_app(stream=True)
