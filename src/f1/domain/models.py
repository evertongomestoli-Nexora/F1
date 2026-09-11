"""Domain models for the F1 dashboard.

Pydantic v2 models mapping the fields relevant to the OpenF1 endpoints
consumed by the ingestion layer (`/meetings`, `/sessions`, `/laps`,
`/drivers`). See `.claude/doc_api.md` for the API contract.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Meeting(BaseModel):
    """A race weekend / event, as returned by `/meetings`."""

    meeting_key: int
    meeting_name: str
    country_name: str
    circuit_short_name: str
    year: int
    date_start: datetime | None = None


class Session(BaseModel):
    """A practice/qualifying/race session, as returned by `/sessions`."""

    session_key: int
    meeting_key: int
    session_name: str
    session_type: str
    date_start: datetime | None = None
    date_end: datetime | None = None
    year: int


class Lap(BaseModel):
    """A single lap, as returned by `/laps`."""

    session_key: int
    driver_number: int
    lap_number: int
    lap_duration: float | None = None
    is_pit_out_lap: bool = False
    date_start: datetime | None = None


class Driver(BaseModel):
    """A driver participating in a session, as returned by `/drivers`."""

    driver_number: int
    session_key: int
    full_name: str
    team_name: str | None = None
    name_acronym: str | None = None


class FastestLapEntry(BaseModel):
    """A processed result row: a driver's best lap in a session."""

    driver_number: int
    driver_name: str
    team_name: str | None = None
    lap_number: int
    lap_duration: float = Field(gt=0)
