"""Unit tests for the SealEngine."""

from __future__ import annotations

from matchcore.engine.core.seal_engine import SealEngine


def test_seal_round_trip_verifies() -> None:
    engine = SealEngine(private_key="test-arbiter-key")
    payload = {"match_id": "M001", "home_id": "C1", "away_id": "C2", "result": {"home_score": 2, "away_score": 1}}
    seal = engine.seal(payload, arbiter_id="ARBITER-0001")
    assert engine.verify(seal, payload) is True


def test_seal_tampered_payload_fails() -> None:
    engine = SealEngine(private_key="test-arbiter-key")
    payload = {"match_id": "M001", "home_id": "C1", "away_id": "C2"}
    seal = engine.seal(payload)
    tampered = dict(payload)
    tampered["home_id"] = "C9"
    assert engine.verify(seal, tampered) is False


def test_chain_hash_links_consecutive_seals() -> None:
    engine = SealEngine(private_key="test-arbiter-key")
    s1 = engine.seal({"i": 1})
    s2 = engine.seal({"i": 2})
    assert s2.prev_chain_hash == s1.chain_hash
    assert s1.chain_hash != s2.chain_hash


def test_root_hash_is_deterministic() -> None:
    e1 = SealEngine(private_key="k1")
    e2 = SealEngine(private_key="k2")
    payload = {"x": 1, "y": [1, 2, 3]}
    assert e1.root_hash(payload) == e2.root_hash(payload)
