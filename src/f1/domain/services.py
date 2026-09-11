"""Application service orchestrating repositories and pure processing functions."""

from __future__ import annotations

from f1.domain.models import FastestLapEntry, Meeting, Session
from f1.domain.repositories import (
    DriverRepository,
    LapRepository,
    MeetingRepository,
    SessionRepository,
)
from f1.processing.lap_processor import build_driver_index, compute_top_n_laps


class F1DashboardService:
    """Orchestrates the four repositories to serve dashboard queries.

    Depends only on the abstract repository interfaces, so any concrete
    implementation (OpenF1 HTTP client, fakes in tests, a future data
    source) can be injected without changing this class.
    """

    def __init__(
        self,
        meeting_repository: MeetingRepository,
        session_repository: SessionRepository,
        lap_repository: LapRepository,
        driver_repository: DriverRepository,
    ) -> None:
        self._meeting_repository = meeting_repository
        self._session_repository = session_repository
        self._lap_repository = lap_repository
        self._driver_repository = driver_repository

    def get_meetings_by_year(self, year: int) -> list[Meeting]:
        """Return all meetings for the given year."""
        return self._meeting_repository.list_by_year(year)

    def get_sessions_by_meeting(self, meeting_key: int) -> list[Session]:
        """Return all sessions for the given meeting."""
        return self._session_repository.list_by_meeting_key(meeting_key)

    def get_top_n_fastest_laps(self, session_key: int, n: int = 10) -> list[FastestLapEntry]:
        """Return the top-N fastest laps (one per driver) for a session."""
        laps = self._lap_repository.list_by_session_key(session_key)
        drivers = self._driver_repository.list_by_session_key(session_key)
        driver_index = build_driver_index(drivers)
        return compute_top_n_laps(laps, driver_index, n=n)
