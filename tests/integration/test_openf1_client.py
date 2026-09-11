"""Integration tests hitting the live OpenF1 API.

Excluded from the default unit test run; execute explicitly with:
    poetry run pytest tests/integration/ -m integration
"""

import pytest

from f1.ingestion.http_client import HttpClient
from f1.ingestion.openf1_client import OpenF1MeetingRepository, OpenF1SessionRepository

pytestmark = pytest.mark.integration


@pytest.fixture
def http_client():
    client = HttpClient(base_url="https://api.openf1.org/v1", timeout_seconds=15)
    yield client
    client.close()


def test_meetings_endpoint_returns_2023_meetings(http_client):
    repo = OpenF1MeetingRepository(http_client)
    meetings = repo.list_by_year(2023)
    assert len(meetings) > 0
    assert all(m.year == 2023 for m in meetings)


def test_sessions_endpoint_returns_sessions_for_a_meeting(http_client):
    meeting_repo = OpenF1MeetingRepository(http_client)
    meetings = meeting_repo.list_by_year(2023)
    session_repo = OpenF1SessionRepository(http_client)

    sessions = session_repo.list_by_meeting_key(meetings[0].meeting_key)

    assert len(sessions) > 0
