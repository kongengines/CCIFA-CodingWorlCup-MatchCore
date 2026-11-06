"""Unit tests for the SovereignLedger."""

from __future__ import annotations

import tempfile

from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


def test_append_and_verify() -> None:
    ledger = SovereignLedger(tempfile.mktemp(suffix=".jsonl"))
    ledger.append({"type": "test", "v": 1})
    ledger.append({"type": "test", "v": 2})
    assert len(ledger) == 2
    assert ledger.verify() is True


def test_chain_links_hold() -> None:
    ledger = SovereignLedger(tempfile.mktemp(suffix=".jsonl"))
    a = ledger.append({"type": "a"})
    b = ledger.append({"type": "b"})
    assert b["prev_hash"] == a["chain_hash"]


def test_query_by_type_and_match() -> None:
    ledger = SovereignLedger(tempfile.mktemp(suffix=".jsonl"))
    ledger.append({"type": "match.official.sealed", "match_id": "M1"})
    ledger.append({"type": "draft.pick", "match_id": None})
    assert len(ledger.query(type="match.official.sealed")) == 1
    assert len(ledger.query(match_id="M1")) == 1
