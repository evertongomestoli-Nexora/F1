"""Unit tests for F1DashboardService, using simple fake repositories that
implement the domain ABCs directly (no unittest.mock)."""

from f1.domain.models import Driver, Lap, Meeting, Session
from f1.domain.repositories import (
    DriverRepository,
    LapRepository,
    MeetingRepository,
    SessionRepository,
)
from f1.domain.services import F1DashboardService


class FakeMeetingRepository(MeetingRepository):
    def __init__(self, meetings: list[Meeting]) -> None:
        self._meetings = meetings

    def list_by_year(self, year: int) -> list[Meeting]:
        return [m for m in self._meetings if m.year == year]


class FakeSessionRepository(SessionRepository):
    def __init__(self, sessions: list[Session]) -> None:
        self._sessions = sessions

    def list_by_meeting_key(self, meeting_key: int) -> list[Session]:
        return [s for s in self._sessions if s.meeting_key == meeting_key]


class FakeLapRepository(LapRepository):
    def __init__(self, laps: list[Lap]) -> None:
        self._laps = laps

    def list_by_session_key(self, session_key: int) -> list[Lap]:
        return [lap for lap in self._laps if lap.session_key == session_key]


class FakeDriverRepository(DriverRepository):
    def __init__(self, drivers: list[Driver]) -> None:
        self._drivers = drivers

    def list_by_session_key(self, session_key: int) -> list[Driver]:
        return [d for d in self._drivers if d.session_key == session_key]


def build_service() -> F1DashboardService:
    meetings = [
        Meeting(
            meeting_key=1,
            meeting_name="Bahrain Grand Prix",
            country_name="Bahrain",
            circuit_short_name="Sakhir",
            year=2023,
        ),
        Meeting(
            meeting_key=2,
            meeting_name="Saudi Arabian Grand Prix",
            country_name="Saudi Arabia",
            circuit_short_name="Jeddah",
            year=2024,
        ),
    ]
    sessions = [
        Session(
            session_key=10,
            meeting_key=1,
            session_name="Race",
            session_type="Race",
            year=2023,
        ),
    ]
    drivers = [
        Driver(driver_number=1, session_key=10, full_name="Driver One", team_name="Team A"),
        Driver(driver_number=2, session_key=10, full_name="Driver Two", team_name="Team B"),
    ]
    laps = [
        Lap(session_key=10, driver_number=1, lap_number=1, lap_duration=92.0),
        Lap(session_key=10, driver_number=1, lap_number=2, lap_duration=89.5),
        Lap(session_key=10, driver_number=2, lap_number=1, lap_duration=90.0),
    ]

    return F1DashboardService(
        meeting_repository=FakeMeetingRepository(meetings),
        session_repository=FakeSessionRepository(sessions),
        lap_repository=FakeLapRepository(laps),
        driver_repository=FakeDriverRepository(drivers),
    )


def test_get_meetings_by_year_filters_correctly():
    service = build_service()
    meetings = service.get_meetings_by_year(2023)
    assert len(meetings) == 1
    assert meetings[0].meeting_name == "Bahrain Grand Prix"


def test_get_sessions_by_meeting_filters_correctly():
    service = build_service()
    sessions = service.get_sessions_by_meeting(1)
    assert len(sessions) == 1
    assert sessions[0].session_name == "Race"


def test_get_top_n_fastest_laps_orchestrates_repositories_and_processing():
    service = build_service()
    top_laps = service.get_top_n_fastest_laps(session_key=10, n=10)

    assert len(top_laps) == 2
    assert top_laps[0].driver_name == "Driver One"
    assert top_laps[0].lap_duration == 89.5
    assert top_laps[1].driver_name == "Driver Two"


def test_get_top_n_fastest_laps_respects_n_limit():
    service = build_service()
    top_laps = service.get_top_n_fastest_laps(session_key=10, n=1)
    assert len(top_laps) == 1
    assert top_laps[0].driver_name == "Driver One"
