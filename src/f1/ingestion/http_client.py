"""Thin HTTP client wrapper over httpx, with retry/backoff and OpenF1 query
param helpers (comparison operators, `latest`, etc. per `.claude/doc_api.md`).
"""

from __future__ import annotations

import time
from typing import Any

import httpx

from f1.utils.logger import get_logger

logger = get_logger(__name__)


class HttpClient:
    """Small HTTP GET client with retry/backoff, scoped to a base URL."""

    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        api_token: str | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}
        self._client = httpx.Client(timeout=timeout_seconds, headers=headers)

    def get(self, path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """GET `path` (relative to base URL) with `params`, retrying on failure.

        Returns the parsed JSON body (OpenF1 endpoints return a JSON array).
        """
        url = f"{self._base_url}/{path.lstrip('/')}"
        last_error: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Request to %s failed (attempt %d/%d): %s",
                    url,
                    attempt,
                    self._max_retries,
                    exc,
                )
                if attempt < self._max_retries:
                    time.sleep(2 ** (attempt - 1))

        logger.error("Request to %s failed after %d attempts", url, self._max_retries)
        raise last_error  # type: ignore[misc]

    def close(self) -> None:
        """Close the underlying httpx client."""
        self._client.close()


def build_query_params(**filters: Any) -> dict[str, Any]:
    """Build OpenF1 query params from keyword filters, dropping `None` values.

    Comparison operators are expressed by embedding them in the key, e.g.
    `build_query_params(**{"date>": "2023-09-15T13:00:00"})`, mirroring the
    OpenF1 API convention documented in `.claude/doc_api.md`.
    """
    return {key: value for key, value in filters.items() if value is not None}
