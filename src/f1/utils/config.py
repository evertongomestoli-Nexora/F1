"""Configuration loader based on environment variables.

No secrets are hardcoded. `.env` (loaded via python-dotenv, if present) can
provide values locally; in deployed environments, real env vars take
precedence.
"""

from __future__ import annotations

import contextlib
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Only load a `.env` that lives at the project root, and never let a
# malformed/unrelated file (e.g. one outside the repo) crash the app.
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DOTENV_PATH = _PROJECT_ROOT / ".env"
if _DOTENV_PATH.is_file():
    with contextlib.suppress(UnicodeDecodeError, OSError):
        load_dotenv(dotenv_path=_DOTENV_PATH)


@dataclass(frozen=True)
class Config:
    """Runtime configuration for the F1 dashboard."""

    openf1_base_url: str
    request_timeout_seconds: float
    max_retries: int
    log_level: str
    openf1_api_token: str | None = None


def load_config() -> Config:
    """Build a `Config` from environment variables, with sensible defaults."""
    return Config(
        openf1_base_url=os.getenv("OPENF1_BASE_URL", "https://api.openf1.org/v1"),
        request_timeout_seconds=float(os.getenv("OPENF1_TIMEOUT_SECONDS", "10")),
        max_retries=int(os.getenv("OPENF1_MAX_RETRIES", "3")),
        log_level=os.getenv("F1_LOG_LEVEL", "INFO"),
        # Optional: only needed for future live-timing endpoints that require auth.
        openf1_api_token=os.getenv("OPENF1_API_TOKEN"),
    )
