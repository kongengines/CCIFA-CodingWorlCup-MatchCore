"""MatchCore CLI — argparse-driven.

Commands:
    init                bootstrap a sovereign engine instance
    federation seed     seed the federation with default confederations
    season simulate     simulate a season + World Cup
    match start         schedule a match
    match seal          seal a finished match
    ledger verify       verify the sovereign ledger
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

from matchcore.engine.core.coder import Coder, CraftDomain
from matchcore.engine.core.club import Club
from matchcore.engine.core.license import LicenseLevel
from matchcore.engine.core.match import Match, MatchKind
from matchcore.engine.core.matchcore import MatchCore


def _engine() -> MatchCore:
    return MatchCore(
        rules_path=os.environ.get("MATCHCORE_RULES_PATH", "matchcore/rules/v1.0"),
        ledger_path=os.environ.get("SEAL_LEDGER_PATH", "matchcore/data/sovereign-ledger.jsonl"),
        arbiter_private_key=os.environ.get("ARBITER_PRIVATE_KEY"),
        arbiter_public_key=os.environ.get("ARBITER_PUBLIC_KEY"),
    )


def cmd_init(args: argparse.Namespace) -> int:
    mc = _engine()
    print(json.dumps({"status": "initialised", "engine": mc.to_dict()}, indent=2))
    return 0


def cmd_federation_seed(args: argparse.Namespace) -> int:
    mc = _engine()
    for arb in ("ARBITER-0001", "ARBITER-0002", "ARBITER-0003"):
        mc.accredit_arbiter(arb)
    print(json.dumps({"federation": mc.federation.to_dict()}, indent=2))
    return 0


def cmd_season_simulate(args: argparse.Namespace) -> int:
    mc = _engine()
    clubs = [mc.register_club(Club(f"C{i:02d}", f"Club {i}", "FRA", budget=1_000_000))
             for i in range(8)]
    coders = [mc.register_coder(Coder(f"P{i:03d}", f"Coder {i}", "FRA",
                                       CraftDomain.CODER, skill=40 + i),
                                level=LicenseLevel.PRO, season=2026)
              for i in range(16)]
    for i, club in enumerate(clubs):
        for c in coders[i*2:(i+1)*2]:
            club.sign(c)
    # schedule + play 4 matches
    for i in range(4):
        m = Match(f"M{i+1:04d}", clubs[i].id, clubs[i+4].id, kind=MatchKind.OFFICIAL)
        mc.schedule_match(m)
        mc.play_match(m.id, home_score=3 + i, away_score=1 + (i % 2),
                      arbiter_id="ARBITER-0001")
    print(json.dumps({
        "clubs": len(mc.clubs), "coders": len(mc.coders),
        "matches": len(mc.matches), "ledger": len(mc.ledger),
        "verified": mc.ledger.verify(),
        "ranking": mc.ranking.to_dict(),
    }, indent=2))
    return 0


def cmd_match_start(args: argparse.Namespace) -> int:
    mc = _engine()
    m = Match(args.match_id, args.home, args.away,
              kind=MatchKind.OFFICIAL, arbiter_id=args.arbiter)
    mc.schedule_match(m)
    print(json.dumps({"scheduled": m.to_dict()}, indent=2))
    return 0


def cmd_match_seal(args: argparse.Namespace) -> int:
    mc = _engine()
    if args.match_id not in mc.matches:
        print(f"Match {args.match_id} not found", file=sys.stderr)
        return 1
    m = mc.matches[args.match_id]
    if not m.is_finished():
        m.start(); m.finish(args.home_score, args.away_score)
    seal = mc.match_engine.seal(m)
    print(json.dumps({"seal": seal.to_dict()}, indent=2))
    return 0


def cmd_ledger_verify(args: argparse.Namespace) -> int:
    mc = _engine()
    ok = mc.ledger.verify()
    print(json.dumps({"verified": ok, **mc.ledger.to_dict()}, indent=2))
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="matchcore", description="CCIFA MatchCore CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="Initialise a sovereign engine").set_defaults(func=cmd_init)

    fed = sub.add_parser("federation", help="Federation commands")
    fed_sub = fed.add_subparsers(dest="subcmd", required=True)
    fed_sub.add_parser("seed", help="Seed federation").set_defaults(func=cmd_federation_seed)

    sea = sub.add_parser("season", help="Season commands")
    sea_sub = sea.add_subparsers(dest="subcmd", required=True)
    sea_sub.add_parser("simulate", help="Simulate a season").set_defaults(func=cmd_season_simulate)

    match_p = sub.add_parser("match", help="Match commands")
    match_sub = match_p.add_subparsers(dest="subcmd", required=True)

    m_start = match_sub.add_parser("start", help="Schedule a match")
    m_start.add_argument("--match-id", required=True)
    m_start.add_argument("--home", required=True)
    m_start.add_argument("--away", required=True)
    m_start.add_argument("--arbiter", default="ARBITER-0001")
    m_start.set_defaults(func=cmd_match_start)

    m_seal = match_sub.add_parser("seal", help="Seal a match")
    m_seal.add_argument("--match-id", required=True)
    m_seal.add_argument("--home-score", type=int, default=1)
    m_seal.add_argument("--away-score", type=int, default=0)
    m_seal.set_defaults(func=cmd_match_seal)

    ledger_p = sub.add_parser("ledger", help="Ledger commands")
    ledger_sub = ledger_p.add_subparsers(dest="subcmd", required=True)
    ledger_sub.add_parser("verify", help="Verify the sovereign ledger").set_defaults(func=cmd_ledger_verify)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
