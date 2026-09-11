"""Concrete OpenF1 repository implementations.

Each repository fetches data via `HttpClient` and validates every item
against the corresponding Pydantic model. An item that fails validation is
logged and skipped, so a single bad API response does not abort the whole
fetch (see CLAUDE.md design decisions).
"""

from __future__ import annotations

from pydantic import ValidationError

from f1.domain.models import Driver, Lap, Meeting, Session
from f1.domain.repositories import (
    DriverRepository,
    LapRepository,
    MeetingRepository,
    SessionRepository,
)
from f1.ingestion.http_client import HttpClient, build_query_params
from f1.utils.logger import get_logger

logger = get_logger(__name__)


class OpenF1MeetingRepository(MeetingRepository):
    """Fetches meetings from the `/meetings` OpenF1 endpoint."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list_by_year(self, year: int) -> list[Meeting]:
        raw_items = self._http_client.get("meetings", build_query_params(year=year))
        return _parse_items(raw_items, Meeting)


class OpenF1SessionRepository(SessionRepository):
    """Fetches sessions from the `/sessions` OpenF1 endpoint."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list_by_meeting_key(self, meeting_key: int) -> list[Session]:
        raw_items = self._http_client.get("sessions", build_query_params(meeting_key=meeting_key))
        return _parse_items(raw_items, Session)


class OpenF1LapRepository(LapRepository):
    """Fetches laps from the `/laps` OpenF1 endpoint."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list_by_session_key(self, session_key: int) -> list[Lap]:
        raw_items = self._http_client.get("laps", build_query_params(session_key=session_key))
        return _parse_items(raw_items, Lap)


class OpenF1DriverRepository(DriverRepository):
    """Fetches drivers from the `/drivers` OpenF1 endpoint."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list_by_session_key(self, session_key: int) -> list[Driver]:
        raw_items = self._http_client.get("drivers", build_query_params(session_key=session_key))
        return _parse_items(raw_items, Driver)


def _parse_items[T](raw_items: list[dict], model: type[T]) -> list[T]:
    """Validate each raw dict against `model`, logging and skipping failures."""
    parsed: list[T] = []
    for raw_item in raw_items:
        try:
            parsed.append(model.model_validate(raw_item))
        except ValidationError as exc:
            logger.warning("Skipping invalid %s item: %s", model.__name__, exc)
    return parsed
