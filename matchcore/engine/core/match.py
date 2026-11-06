"""Matches — the atomic unit of competition.

A match opposes two teams (home/away), is either ``OFFICIAL`` or
``FRIENDLY``, and once finished carries a :class:`MatchResult` plus,
for official matches, a :class:`SovereignSeal`.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from matchcore.engine.core.seal_engine import SovereignSeal


class MatchKind(str, Enum):
    OFFICIAL = "OFFICIAL"
    FRIENDLY = "FRIENDLY"


class MatchStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class MatchResult:
    """The final score and outcome of a finished match."""

    __slots__ = ("home_score", "away_score", "winner_id", "finished_at")

    def __init__(self, home_score: int, away_score: int,
                 *, finished_at: Optional[datetime] = None) -> None:
        self.home_score = home_score
        self.away_score = away_score
        self.winner_id: Optional[str] = None
        if home_score > away_score:
            self.winner_id = "home"
        elif away_score > home_score:
            self.winner_id = "away"
        self.finished_at = finished_at or datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "home_score": self.home_score,
            "away_score": self.away_score,
            "winner_id": self.winner_id,
            "finished_at": self.finished_at.isoformat(),
        }


class Match:
    """A CCIFA match."""

    def __init__(self, match_id: str, home_id: str, away_id: str, *,
                 kind: MatchKind | str = MatchKind.OFFICIAL,
                 scheduled_at: Optional[datetime] = None,
                 arbiter_id: Optional[str] = None,
                 arena_node_id: Optional[str] = None) -> None:
        self.id = match_id
        self.home_id = home_id
        self.away_id = away_id
        self.kind = MatchKind(kind) if isinstance(kind, str) else kind
        self.scheduled_at = scheduled_at or datetime.now(timezone.utc)
        self.arbiter_id = arbiter_id
        self.arena_node_id = arena_node_id
        self.status = MatchStatus.SCHEDULED
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None
        self.result: Optional[MatchResult] = None
        self.seal: Optional[SovereignSeal] = None
        self.submissions: list[Dict[str, Any]] = []

    # -- lifecycle ------------------------------------------------------ #
    def start(self) -> "Match":
        if self.status is not MatchStatus.SCHEDULED:
            raise ValueError(f"Cannot start match in status {self.status.value}")
        self.status = MatchStatus.IN_PROGRESS
        self.started_at = datetime.now(timezone.utc)
        return self

    def play(self, home_score: int, away_score: int,
             *, arbiter_id: Optional[str] = None) -> MatchResult:
        """One-shot play: start, finish, return result (no seal)."""
        if self.status is MatchStatus.SCHEDULED:
            self.start()
        if arbiter_id:
            self.arbiter_id = arbiter_id
        return self.finish(home_score, away_score)

    def finish(self, home_score: int, away_score: int) -> MatchResult:
        if self.status is not MatchStatus.IN_PROGRESS:
            raise ValueError(f"Cannot finish match in status {self.status.value}")
        self.result = MatchResult(home_score, away_score)
        self.status = MatchStatus.FINISHED
        self.finished_at = datetime.now(timezone.utc)
        return self.result

    def attach_seal(self, seal: SovereignSeal) -> None:
        if self.kind is not MatchKind.OFFICIAL:
            raise ValueError("Only official matches can be sealed")
        if self.status is not MatchStatus.FINISHED:
            raise ValueError("Match must be finished before sealing")
        self.seal = seal

    def is_finished(self) -> bool:
        return self.status is MatchStatus.FINISHED

    def is_official(self) -> bool:
        return self.kind is MatchKind.OFFICIAL

    # -- canonical payload (for hashing) ------------------------------- #
    def canonical_payload(self) -> Dict[str, Any]:
        """The canonical, deterministic dict used by the SealEngine."""
        return {
            "match_id": self.id,
            "home_id": self.home_id,
            "away_id": self.away_id,
            "kind": self.kind.value,
            "scheduled_at": self.scheduled_at.isoformat(),
            "arbiter_id": self.arbiter_id,
            "arena_node_id": self.arena_node_id,
            "result": self.result.to_dict() if self.result else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
        }

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "home_id": self.home_id,
            "away_id": self.away_id,
            "kind": self.kind.value,
            "status": self.status.value,
            "scheduled_at": self.scheduled_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "arbiter_id": self.arbiter_id,
            "arena_node_id": self.arena_node_id,
            "result": self.result.to_dict() if self.result else None,
            "seal": self.seal.to_dict() if self.seal else None,
        }

    def __repr__(self) -> str:
        return f"<Match {self.id} {self.kind.value} {self.status.value}>"
