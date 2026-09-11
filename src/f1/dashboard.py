"""Streamlit composition root.

Wires HttpClient -> concrete OpenF1 repositories -> F1DashboardService and
renders the UI. No business logic lives here; it all belongs in
`domain/` and `processing/`.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from f1.domain.services import F1DashboardService
from f1.ingestion.http_client import HttpClient
from f1.ingestion.openf1_client import (
    OpenF1DriverRepository,
    OpenF1LapRepository,
    OpenF1MeetingRepository,
    OpenF1SessionRepository,
)
from f1.utils.config import load_config


@st.cache_resource
def get_service() -> F1DashboardService:
    """Build (once per process) the HTTP client, repositories and service."""
    config = load_config()
    http_client = HttpClient(
        base_url=config.openf1_base_url,
        timeout_seconds=config.request_timeout_seconds,
        max_retries=config.max_retries,
        api_token=config.openf1_api_token,
    )
    return F1DashboardService(
        meeting_repository=OpenF1MeetingRepository(http_client),
        session_repository=OpenF1SessionRepository(http_client),
        lap_repository=OpenF1LapRepository(http_client),
        driver_repository=OpenF1DriverRepository(http_client),
    )


@st.cache_data(ttl=300)
def fetch_meetings(year: int) -> list[dict]:
    """Cached lookup of meetings for a year, as plain dicts (cache-friendly)."""
    service = get_service()
    return [meeting.model_dump() for meeting in service.get_meetings_by_year(year)]


@st.cache_data(ttl=300)
def fetch_sessions(meeting_key: int) -> list[dict]:
    """Cached lookup of sessions for a meeting, as plain dicts."""
    service = get_service()
    return [session.model_dump() for session in service.get_sessions_by_meeting(meeting_key)]


@st.cache_data(ttl=300)
def fetch_top_laps(session_key: int, top_n: int) -> list[dict]:
    """Cached lookup of the fastest laps for a session, as plain dicts."""
    service = get_service()
    return [entry.model_dump() for entry in service.get_top_n_fastest_laps(session_key, n=top_n)]


def main() -> None:
    """Render the Streamlit dashboard."""
    st.set_page_config(page_title="F1 Dashboard", layout="wide")
    st.title("F1 Dashboard - Voltas mais rapidas (OpenF1)")

    year = st.sidebar.number_input("Ano", min_value=2023, max_value=2100, value=2023, step=1)
    meetings = fetch_meetings(int(year))
    if not meetings:
        st.info("Nenhum evento encontrado para este ano.")
        return

    meeting_options = {m["meeting_name"]: m["meeting_key"] for m in meetings}
    meeting_name = st.sidebar.selectbox("Evento", list(meeting_options.keys()))
    meeting_key = meeting_options[meeting_name]

    sessions = fetch_sessions(meeting_key)
    if not sessions:
        st.info("Nenhuma sessao encontrada para este evento.")
        return

    session_options = {s["session_name"]: s["session_key"] for s in sessions}
    session_name = st.sidebar.selectbox("Sessao", list(session_options.keys()))
    session_key = session_options[session_name]

    top_n = st.sidebar.slider("Top N pilotos", min_value=1, max_value=20, value=10)

    top_laps = fetch_top_laps(session_key, top_n)
    if not top_laps:
        st.info("Nenhuma volta valida encontrada para esta sessao.")
        return

    st.subheader(f"Top {top_n} voltas mais rapidas - {meeting_name} / {session_name}")
    st.dataframe(pd.DataFrame(top_laps), use_container_width=True)


if __name__ == "__main__":
    main()
