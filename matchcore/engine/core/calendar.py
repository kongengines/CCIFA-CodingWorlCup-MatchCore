"""Match calendars.

A calendar is an ordered collection of matches; it can be filtered by
date, by kind (official / friendly) and queried for upcoming/past.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List

from matchcore.engine.core.match import Match, MatchKind


class Calendar:
    """A league or tournament calendar."""

    def __init__(self, matches: List[Match] | None = None) -> None:
        self.matches: List[Match] = list(matches or [])

    def add(self, match: Match) -> None:
        self.matches.append(match)

    def by_date(self, day: date) -> List[Match]:
        return [m for m in self.matches if m.scheduled_at.date() == day]

    def official_only(self) -> List[Match]:
        return [m for m in self.matches if m.kind is MatchKind.OFFICIAL]

    def friendly_only(self) -> List[Match]:
        return [m for m in self.matches if m.kind is MatchKind.FRIENDLY]

    def upcoming(self, *, now: datetime | None = None) -> List[Match]:
        now = now or datetime.utcnow()
        return sorted([m for m in self.matches if m.scheduled_at >= now and not m.is_finished()],
                      key=lambda m: m.scheduled_at)

    def played(self) -> List[Match]:
        return [m for m in self.matches if m.is_finished()]

    def to_dict(self) -> List[Dict[str, Any]]:
        return [m.to_dict() for m in self.matches]

    def __len__(self) -> int:
        return len(self.matches)

    def __repr__(self) -> str:
        return f"<Calendar {len(self.matches)} matches>"
