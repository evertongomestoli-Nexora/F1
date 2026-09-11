"""Abstract repository interfaces for all data access.

Concrete implementations live in `f1.ingestion`. The domain layer depends
only on these abstractions, never on a concrete data source.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from f1.domain.models import Driver, Lap, Meeting, Session


class MeetingRepository(ABC):
    """Provides access to meeting (race weekend) data."""

    @abstractmethod
    def list_by_year(self, year: int) -> list[Meeting]:
        """Return all meetings held in the given year."""


class SessionRepository(ABC):
    """Provides access to session data."""

    @abstractmethod
    def list_by_meeting_key(self, meeting_key: int) -> list[Session]:
        """Return all sessions belonging to a meeting."""


class LapRepository(ABC):
    """Provides access to lap data."""

    @abstractmethod
    def list_by_session_key(self, session_key: int) -> list[Lap]:
        """Return all laps recorded for a session."""


class DriverRepository(ABC):
    """Provides access to driver data."""

    @abstractmethod
    def list_by_session_key(self, session_key: int) -> list[Driver]:
        """Return all drivers who participated in a session."""
