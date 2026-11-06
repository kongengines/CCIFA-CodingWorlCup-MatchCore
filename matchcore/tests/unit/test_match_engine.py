"""Unit tests for the MatchEngine lifecycle."""

from __future__ import annotations

import tempfile

from matchcore.engine.core.match import Match, MatchKind
from matchcore.engine.core.match_engine import MatchEngine
from matchcore.engine.core.seal_engine import SealEngine
from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


def _engine() -> MatchEngine:
    seal = SealEngine(private_key="arbiter-test-key")
    ledger = SovereignLedger(tempfile.mktemp(suffix=".jsonl"))
    return MatchEngine(seal, ledger)


def test_official_match_is_sealed() -> None:
    me = _engine()
    m = Match("M-001", "C1", "C2", kind=MatchKind.OFFICIAL)
    me.run(m, home_score=3, away_score=1, arbiter_id="ARBITER-0001")
    assert m.is_finished()
    assert m.seal is not None
    assert m.seal.arbiter_id == "ARBITER-0001"
    assert me.seal_engine.verify(m.seal, m.canonical_payload()) is True


def test_friendly_match_not_sealed() -> None:
    me = _engine()
    m = Match("M-002", "C1", "C2", kind=MatchKind.FRIENDLY)
    me.run(m, home_score=2, away_score=2, arbiter_id="ARBITER-0001")
    assert m.is_finished()
    assert m.seal is None


def test_ledger_grows_per_event() -> None:
    me = _engine()
    m1 = Match("M-A", "C1", "C2", kind=MatchKind.OFFICIAL)
    m2 = Match("M-B", "C3", "C4", kind=MatchKind.OFFICIAL)
    me.run(m1, 1, 0, arbiter_id="ARBITER-0001")
    me.run(m2, 2, 2, arbiter_id="ARBITER-0001")
    assert len(me.ledger) == 2
    assert me.ledger.verify() is True
