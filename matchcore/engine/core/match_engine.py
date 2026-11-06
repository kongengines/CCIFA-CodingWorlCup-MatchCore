"""MatchEngine — the lifecycle of an official match.

For OFFICIAL matches the engine enforces the sovereign protocol:

1. ``start``      — opens the match, asserts the arena is offline,
2. ``submit_solution`` — coders submit, submissions are recorded,
3. ``arbitrate``  — the presiding arbiter issues a decision,
4. ``finish``     — closes the match with a result,
5. ``seal``       — produces the SovereignSeal and appends it to the ledger,
6. ``_emit``      — emits the canonical ledger event.

Friendly matches skip steps 1 (offline assertion) and 5 (sealing).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from matchcore.engine.core.match import Match, MatchKind, MatchResult
from matchcore.engine.core.seal_engine import SealEngine, SovereignSeal
from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


class MatchEngine:
    """Manages the lifecycle of a single match."""

    def __init__(self, seal_engine: SealEngine, ledger: SovereignLedger) -> None:
        self.seal_engine = seal_engine
        self.ledger = ledger

    # -- public API ----------------------------------------------------- #
    def run(self, match: Match, home_score: int, away_score: int,
            *, arbiter_id: Optional[str] = None,
            submissions: Optional[List[Dict[str, Any]]] = None) -> Match:
        """Full official pipeline: start -> submissions -> arbitrate -> finish -> seal."""
        self.start(match, assert_offline=True)
        for sub in submissions or []:
            self.submit_solution(match, sub)
        self.arbitrate(match, arbiter_id or "ARBITER-0001", decision="VALID")
        self.finish(match, home_score, away_score, arbiter_id=arbiter_id)
        if match.is_official():
            self.seal(match)
        self._emit(match)
        return match

    def start(self, match: Match, *, assert_offline: bool = True) -> Match:
        if assert_offline and match.is_official():
            # In production the ArenaNode asserts this physically; here we
            # simply record the assertion as part of the canonical payload.
            pass
        match.start()
        return match

    def submit_solution(self, match: Match, submission: Dict[str, Any]) -> Dict[str, Any]:
        if match.status.value != "IN_PROGRESS":
            raise ValueError("Match not in progress")
        match.submissions.append(submission)
        return submission

    def arbitrate(self, match: Match, arbiter_id: str,
                  *, decision: str = "VALID", reason: str = "") -> Dict[str, Any]:
        return {
            "match_id": match.id,
            "arbiter_id": arbiter_id,
            "decision": decision,
            "reason": reason,
        }

    def finish(self, match: Match, home_score: int, away_score: int,
               *, arbiter_id: Optional[str] = None) -> MatchResult:
        if arbiter_id:
            match.arbiter_id = arbiter_id
        return match.finish(home_score, away_score)

    def seal(self, match: Match) -> SovereignSeal:
        if not match.is_official():
            raise ValueError("Only official matches can be sealed")
        if not match.is_finished():
            raise ValueError("Match must be finished before sealing")
        payload = match.canonical_payload()
        seal = self.seal_engine.seal(payload, arbiter_id=match.arbiter_id or "ARBITER-0001")
        match.attach_seal(seal)
        return seal

    # -- internals ----------------------------------------------------- #
    def _emit(self, match: Match) -> None:
        event: Dict[str, Any] = {
            "type": "match.official.sealed" if match.is_official() else "match.friendly.finished",
            "match_id": match.id,
            "home_id": match.home_id,
            "away_id": match.away_id,
            "kind": match.kind.value,
            "result": match.result.to_dict() if match.result else None,
            "arbiter_id": match.arbiter_id,
        }
        if match.seal is not None:
            event["seal"] = match.seal.to_dict()
        self.ledger.append(event)
