#!/usr/bin/env python3
"""Seed the MatchCore instance with sample federation, clubs, coders and a few matches."""

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


def main() -> None:
    mc = MatchCore(
        rules_path=None,
        ledger_path=tempfile.mktemp(suffix=".jsonl"),
        arbiter_private_key="seed-key",
    )
    mc.accredit_arbiter("ARBITER-0001")
    clubs = [mc.register_club(Club(f"C{i:02d}", f"Club {i}", "FRA", budget=1_000_000))
             for i in range(4)]
    for i in range(8):
        mc.register_coder(
            Coder(f"P{i:03d}", f"Coder {i}", "FRA",
                  CraftDomain.CODER, skill=50 + i),
            level=LicenseLevel.PRO, season=2026,
        )
    for i, club in enumerate(clubs):
        for c in list(mc.coders.values())[i * 2:(i + 1) * 2]:
            club.sign(c)
    for i in range(2):
        m = Match(f"SEED-M{i+1}", clubs[i].id, clubs[i + 2].id, kind=MatchKind.OFFICIAL)
        mc.schedule_match(m)
        mc.play_match(m.id, home_score=2 + i, away_score=1, arbiter_id="ARBITER-0001")
    print(json.dumps({"seeded": True, "engine": mc.to_dict()}, indent=2))


if __name__ == "__main__":
    main()
