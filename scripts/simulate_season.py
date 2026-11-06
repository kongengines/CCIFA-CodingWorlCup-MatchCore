#!/usr/bin/env python3
"""Simulate a full season + World Cup final via the MatchCore orchestrator."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from matchcore.engine.core.coder import Coder, CraftDomain
from matchcore.engine.core.club import Club
from matchcore.engine.core.license import LicenseLevel
from matchcore.engine.core.match import Match, MatchKind
from matchcore.engine.core.matchcore import MatchCore


def main() -> int:
    mc = MatchCore(
        rules_path=None,
        ledger_path=tempfile.mktemp(suffix=".jsonl"),
        arbiter_private_key="season-cli-key",
    )
    mc.accredit_arbiter("ARBITER-0001")
    clubs = [mc.register_club(Club(f"C{i:02d}", f"Club {i}", "FRA", budget=1_000_000))
             for i in range(8)]
    crafts = [CraftDomain.CODER, CraftDomain.DESIGNER, CraftDomain.MAKER, CraftDomain.STRATEGIST]
    for i in range(16):
        mc.register_coder(
            Coder(f"P{i:03d}", f"Coder {i}", "FRA", crafts[i % 4], skill=40 + i),
            level=LicenseLevel.PRO, season=2026,
        )
    for i, club in enumerate(clubs):
        for c in list(mc.coders.values())[i * 2:(i + 1) * 2]:
            club.sign(c)
    for i in range(8):
        home = clubs[i].id
        away = clubs[(i + 1) % 8].id
        m = Match(f"S2026-M{i+1:02d}", home, away, kind=MatchKind.OFFICIAL)
        mc.schedule_match(m)
        mc.play_match(m.id, home_score=3 - (i % 3), away_score=i % 3,
                       arbiter_id="ARBITER-0001")
    final = Match("WC-2026-FINAL", clubs[0].id, clubs[4].id, kind=MatchKind.OFFICIAL)
    mc.schedule_match(final)
    mc.play_match(final.id, home_score=5, away_score=2, arbiter_id="ARBITER-0001")
    print(json.dumps({
        "clubs": len(mc.clubs),
        "coders": len(mc.coders),
        "matches": len(mc.matches),
        "ledger_entries": len(mc.ledger),
        "ledger_verified": mc.ledger.verify(),
        "ranking": mc.ranking.to_dict(),
        "final_seal": final.seal.to_dict() if final.seal else None,
    }, indent=2))
    return 0 if mc.ledger.verify() else 1


if __name__ == "__main__":
    raise SystemExit(main())
