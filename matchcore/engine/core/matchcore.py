"""MatchCore — the orchestrator.

MatchCore ties together the federation, leagues, clubs, coders,
arbitration, drafts, transfers, the calendar, the seal engine and the
sovereign ledger. It is the only entry point used by the REST API and
the CLI.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from matchcore.engine.core.arbitration import Arbitration, ArbiterDecision
from matchcore.engine.core.calendar import Calendar
from matchcore.engine.core.club import Club
from matchcore.engine.core.coder import Coder, CraftDomain
from matchcore.engine.core.draft import Draft
from matchcore.engine.core.federation import Federation
from matchcore.engine.core.license import License, LicenseLevel
from matchcore.engine.core.match import Match, MatchKind, MatchResult
from matchcore.engine.core.match_engine import MatchEngine
from matchcore.engine.core.ranking import Ranking
from matchcore.engine.core.rule_engine import RuleEngine
from matchcore.engine.core.seal_engine import SealEngine
from matchcore.engine.core.transfer import Transfer, TransferWindow
from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


class MatchCore:
    """The sovereign engine."""

    def __init__(self, *, rules_path: Optional[str] = None,
                 ledger_path: Optional[str] = None,
                 arbiter_private_key: Optional[str] = None,
                 arbiter_public_key: Optional[str] = None) -> None:
        self.federation = Federation()
        self.clubs: Dict[str, Club] = {}
        self.coders: Dict[str, Coder] = {}
        self.leagues: Dict[str, Any] = {}
        self.drafts: Dict[str, Draft] = {}
        self.transfers: Dict[str, Transfer] = {}
        self.matches: Dict[str, Match] = {}
        self.calendar = Calendar()
        self.arbitration = Arbitration()
        self.ranking = Ranking()

        rules_path = rules_path or os.environ.get(
            "MATCHCORE_RULES_PATH", "matchcore/rules/v1.0")
        self.rules = RuleEngine(rules_path)

        ledger_path = ledger_path or os.environ.get(
            "SEAL_LEDGER_PATH", "matchcore/data/sovereign-ledger.jsonl")
        self.ledger = SovereignLedger(ledger_path)

        self.seal_engine = SealEngine(
            private_key=arbiter_private_key,
            public_key=arbiter_public_key,
            genesis_hash=os.environ.get(
                "SEAL_GENESIS_HASH",
                "0" * 64),
        )
        self.match_engine = MatchEngine(self.seal_engine, self.ledger)
        self.created_at = datetime.now(timezone.utc)

    # -- registry ------------------------------------------------------- #
    def register_club(self, club: Club) -> Club:
        self.clubs[club.id] = club
        return club

    def register_coder(self, coder: Coder, *,
                       level: LicenseLevel | str = LicenseLevel.AMATEUR,
                       season: Optional[int] = None) -> Coder:
        self.coders[coder.id] = coder
        season = season or datetime.now(timezone.utc).year
        lic = self.federation.issue_license(level, coder.id, season)
        coder.license = lic
        return coder

    def accredit_arbiter(self, arbiter_id: str) -> None:
        self.federation.accredit_arbiter(arbiter_id)
        self.arbitration.accredit(arbiter_id)

    # -- matches -------------------------------------------------------- #
    def schedule_match(self, match: Match) -> Match:
        self.matches[match.id] = match
        self.calendar.add(match)
        return match

    def play_match(self, match_id: str, home_score: int, away_score: int,
                   *, arbiter_id: Optional[str] = None) -> Match:
        match = self.matches[match_id]
        if match.is_official():
            self.match_engine.run(match, home_score, away_score,
                                  arbiter_id=arbiter_id or self.arbitration.presiding())
        else:
            match.play(home_score, away_score, arbiter_id=arbiter_id)
            self.ledger.append({
                "type": "match.friendly.finished",
                "match_id": match.id,
                "result": match.result.to_dict() if match.result else None,
            })
        # Update the live ranking.
        if match.result is not None:
            r = match.result
            if r.home_score > r.away_score:
                self.ranking.update(match.home_id, 3, "W", gf=r.home_score, ga=r.away_score)
                self.ranking.update(match.away_id, 0, "L", gf=r.away_score, ga=r.home_score)
            elif r.home_score < r.away_score:
                self.ranking.update(match.away_id, 3, "W", gf=r.away_score, ga=r.home_score)
                self.ranking.update(match.home_id, 0, "L", gf=r.home_score, ga=r.away_score)
            else:
                self.ranking.update(match.home_id, 1, "D", gf=r.home_score, ga=r.away_score)
                self.ranking.update(match.away_id, 1, "D", gf=r.away_score, ga=r.home_score)
        return match

    # -- drafts --------------------------------------------------------- #
    def create_draft(self, season: int, eligible: List[Coder]) -> Draft:
        draft = Draft(f"DRAFT-{season}", season)
        draft.set_eligible(eligible)
        draft.compute_order(self.ranking.to_dict())
        self.drafts[draft.id] = draft
        return draft

    def draft_pick(self, draft_id: str, club_id: str, coder_id: str) -> Dict[str, Any]:
        draft = self.drafts[draft_id]
        record = draft.pick(club_id, coder_id)
        coder = self.coders[coder_id]
        if coder and club_id in self.clubs:
            self.clubs[club_id].sign(coder)
        self.ledger.append({"type": "draft.pick", **record})
        return record

    # -- transfers ------------------------------------------------------ #
    def open_transfer(self, coder_id: str, from_club_id: str, to_club_id: str,
                      *, fee: int = 0, window: Optional[TransferWindow] = None) -> Transfer:
        t = Transfer(f"TR-{len(self.transfers)+1:06d}", coder_id,
                     from_club_id, to_club_id, fee=fee, window=window)
        self.transfers[t.id] = t
        return t

    def complete_transfer(self, transfer_id: str) -> Transfer:
        t = self.transfers[transfer_id]
        t.validate()
        t.complete()
        coder = self.coders.get(t.coder_id)
        if coder and t.from_club_id in self.clubs and t.to_club_id in self.clubs:
            self.clubs[t.from_club_id].release(t.coder_id)
            self.clubs[t.to_club_id].sign(coder)
        self.ledger.append({"type": "transfer.completed", **t.to_dict()})
        return t

    # -- arbitration ---------------------------------------------------- #
    def arbiter_decision(self, arbiter_id: str, decision: ArbiterDecision,
                         target_id: str, **kwargs: Any) -> Dict[str, Any]:
        d = self.arbitration.decide(arbiter_id, decision, target_id, **kwargs)
        self.ledger.append({"type": "arbitration.decision", **d.to_dict()})
        return d.to_dict()

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "federation": self.federation.to_dict(),
            "clubs": len(self.clubs),
            "coders": len(self.coders),
            "leagues": list(self.leagues.keys()),
            "drafts": {k: v.to_dict() for k, v in self.drafts.items()},
            "transfers": {k: v.to_dict() for k, v in self.transfers.items()},
            "matches": len(self.matches),
            "calendar_size": len(self.calendar),
            "ranking": self.ranking.to_dict(),
            "arbitration": self.arbitration.to_dict(),
            "rules_version": self.rules.version,
            "ledger_entries": len(self.ledger),
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return (f"<MatchCore clubs={len(self.clubs)} coders={len(self.coders)} "
                f"matches={len(self.matches)} ledger={len(self.ledger)}>")
