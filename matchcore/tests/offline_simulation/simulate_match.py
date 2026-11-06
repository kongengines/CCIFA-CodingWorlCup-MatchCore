"""Offline match simulation — runs an official match end-to-end and prints the seal."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from matchcore.engine.core.match import Match, MatchKind
from matchcore.engine.core.match_engine import MatchEngine
from matchcore.engine.core.seal_engine import SealEngine
from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


def main() -> None:
    seal = SealEngine(private_key="arena-demo-key")
    ledger = SovereignLedger(tempfile.mktemp(suffix=".jsonl"))
    me = MatchEngine(seal, ledger)
    m = Match("M-DEMO-001", "C01-Phoenix", "C02-Atlas", kind=MatchKind.OFFICIAL,
              arbiter_id="ARBITER-0001")
    me.run(m, home_score=4, away_score=2, arbiter_id="ARBITER-0001")
    print("=== OFFICIAL MATCH SIMULATION ===")
    print(json.dumps(m.to_dict(), indent=2))
    print("=== LEDGER ===")
    print(json.dumps(ledger.to_dict(), indent=2))
    print("=== VERIFIED ===", ledger.verify())


if __name__ == "__main__":
    main()
