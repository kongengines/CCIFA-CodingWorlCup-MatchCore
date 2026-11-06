"""Arbitration — arbiters and their decisions.

Arbiters are accredited by the federation. During an official match,
exactly one presiding arbiter signs the Sovereign Seal. Arbiters can
issue four kinds of decisions.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class ArbiterDecision(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    PENALTY = "PENALTY"
    DISQUALIFY = "DISQUALIFY"


class Decision:
    """A single arbiter decision."""

    def __init__(self, arbiter_id: str, decision: ArbiterDecision,
                 target_id: str, *, reason: str = "",
                 penalty_points: int = 0) -> None:
        self.id = uuid.uuid4().hex[:12]
        self.arbiter_id = arbiter_id
        self.decision = decision
        self.target_id = target_id
        self.reason = reason
        self.penalty_points = penalty_points
        self.issued_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "arbiter_id": self.arbiter_id,
            "decision": self.decision.value,
            "target_id": self.target_id,
            "reason": self.reason,
            "penalty_points": self.penalty_points,
            "issued_at": self.issued_at.isoformat(),
        }


class Arbitration:
    """The arbitration subsystem for a match or a league."""

    def __init__(self) -> None:
        self.arbiters: List[str] = []
        self.decisions: List[Decision] = []

    def accredit(self, arbiter_id: str) -> None:
        if arbiter_id not in self.arbiters:
            self.arbiters.append(arbiter_id)

    def decide(self, arbiter_id: str, decision: ArbiterDecision,
               target_id: str, *, reason: str = "",
               penalty_points: int = 0) -> Decision:
        if arbiter_id not in self.arbiters:
            raise ValueError(f"Arbiter {arbiter_id} not accredited")
        d = Decision(arbiter_id, decision, target_id, reason=reason,
                     penalty_points=penalty_points)
        self.decisions.append(d)
        return d

    def for_target(self, target_id: str) -> List[Decision]:
        return [d for d in self.decisions if d.target_id == target_id]

    def presiding(self) -> Optional[str]:
        return self.arbiters[0] if self.arbiters else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "arbiters": list(self.arbiters),
            "decisions": [d.to_dict() for d in self.decisions],
            "presiding": self.presiding(),
        }
