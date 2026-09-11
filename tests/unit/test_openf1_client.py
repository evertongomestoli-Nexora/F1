"""Unit tests for the OpenF1 repository implementations, using a fake
HttpClient so no network calls are made."""

from f1.ingestion.http_client import build_query_params
from f1.ingestion.openf1_client import (
    OpenF1DriverRepository,
    OpenF1LapRepository,
    OpenF1MeetingRepository,
    OpenF1SessionRepository,
)


class FakeHttpClient:
    def __init__(self, response: list[dict]) -> None:
        self.response = response
        self.last_path = None
        self.last_params = None

    def get(self, path, params=None):
        self.last_path = path
        self.last_params = params
        return self.response


def test_build_query_params_drops_none_values():
    params = build_query_params(year=2023, country_name=None)
    assert params == {"year": 2023}


def test_meeting_repository_parses_valid_and_skips_invalid_items():
    fake_client = FakeHttpClient(
        [
            {
                "meeting_key": 1,
                "meeting_name": "Bahrain Grand Prix",
                "country_name": "Bahrain",
                "circuit_short_name": "Sakhir",
                "year": 2023,
            },
            {"meeting_key": "not-an-int-but-fails-other-fields"},
        ]
    )
    repo = OpenF1MeetingRepository(fake_client)  # type: ignore[arg-type]

    meetings = repo.list_by_year(2023)

    assert len(meetings) == 1
    assert meetings[0].meeting_name == "Bahrain Grand Prix"
    assert fake_client.last_path == "meetings"
    assert fake_client.last_params == {"year": 2023}


def test_session_repository_calls_expected_endpoint():
    fake_client = FakeHttpClient(
        [
            {
                "session_key": 10,
                "meeting_key": 1,
                "session_name": "Race",
                "session_type": "Race",
                "year": 2023,
            }
        ]
    )
    repo = OpenF1SessionRepository(fake_client)  # type: ignore[arg-type]

    sessions = repo.list_by_meeting_key(1)

    assert len(sessions) == 1
    assert fake_client.last_path == "sessions"


def test_lap_repository_calls_expected_endpoint():
    fake_client = FakeHttpClient(
        [{"session_key": 10, "driver_number": 1, "lap_number": 1, "lap_duration": 90.0}]
    )
    repo = OpenF1LapRepository(fake_client)  # type: ignore[arg-type]

    laps = repo.list_by_session_key(10)

    assert len(laps) == 1
    assert fake_client.last_path == "laps"


def test_driver_repository_calls_expected_endpoint():
    fake_client = FakeHttpClient(
        [{"driver_number": 1, "session_key": 10, "full_name": "Driver One"}]
    )
    repo = OpenF1DriverRepository(fake_client)  # type: ignore[arg-type]

    drivers = repo.list_by_session_key(10)

    assert len(drivers) == 1
    assert fake_client.last_path == "drivers"
