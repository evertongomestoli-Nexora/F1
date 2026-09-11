"""Unit tests for Pydantic domain models, using example payloads shaped like
the OpenF1 endpoints described in `.claude/doc_api.md`."""

import pytest
from pydantic import ValidationError

from f1.domain.models import Driver, FastestLapEntry, Lap, Meeting, Session


def test_meeting_parses_openf1_payload():
    payload = {
        "meeting_key": 1219,
        "meeting_name": "Bahrain Grand Prix",
        "country_name": "Bahrain",
        "circuit_short_name": "Sakhir",
        "year": 2023,
        "date_start": "2023-03-03T13:30:00+00:00",
    }
    meeting = Meeting.model_validate(payload)
    assert meeting.meeting_key == 1219
    assert meeting.year == 2023


def test_session_parses_openf1_payload():
    payload = {
        "session_key": 9159,
        "meeting_key": 1219,
        "session_name": "Race",
        "session_type": "Race",
        "date_start": "2023-03-05T15:00:00+00:00",
        "date_end": "2023-03-05T17:00:00+00:00",
        "year": 2023,
    }
    session = Session.model_validate(payload)
    assert session.session_key == 9159
    assert session.session_name == "Race"


def test_lap_parses_openf1_payload_and_defaults_pit_out_lap():
    payload = {
        "session_key": 9159,
        "driver_number": 1,
        "lap_number": 5,
        "lap_duration": 91.023,
        "date_start": "2023-03-05T15:10:00+00:00",
    }
    lap = Lap.model_validate(payload)
    assert lap.is_pit_out_lap is False
    assert lap.lap_duration == 91.023


def test_driver_parses_openf1_payload():
    payload = {
        "driver_number": 1,
        "session_key": 9159,
        "full_name": "Max Verstappen",
        "team_name": "Red Bull Racing",
        "name_acronym": "VER",
    }
    driver = Driver.model_validate(payload)
    assert driver.full_name == "Max Verstappen"
    assert driver.name_acronym == "VER"


def test_fastest_lap_entry_requires_positive_duration():
    with pytest.raises(ValidationError):
        FastestLapEntry(
            driver_number=1,
            driver_name="Max Verstappen",
            team_name="Red Bull Racing",
            lap_number=5,
            lap_duration=0,
        )


def test_meeting_missing_required_field_raises():
    with pytest.raises(ValidationError):
        Meeting.model_validate({"meeting_key": 1219})
