"""Core domain models for MatchCore.

Every class in this package is plain Python (no I/O, no framework) so it
can be exercised by unit tests, the CLI and the FastAPI layer alike.
"""

from matchcore.engine.core.federation import Federation
from matchcore.engine.core.confederation import Confederation
from matchcore.engine.core.league import League
from matchcore.engine.core.club import Club
from matchcore.engine.core.coder import Coder, CraftDomain
from matchcore.engine.core.license import License, LicenseLevel
from matchcore.engine.core.draft import Draft
from matchcore.engine.core.transfer import Transfer
from matchcore.engine.core.calendar import Calendar
from matchcore.engine.core.match import Match, MatchKind, MatchResult
from matchcore.engine.core.arbitration import Arbitration, ArbiterDecision
from matchcore.engine.core.ranking import Ranking
from matchcore.engine.core.matchcore import MatchCore
from matchcore.engine.core.match_engine import MatchEngine
from matchcore.engine.core.rule_engine import RuleEngine
from matchcore.engine.core.seal_engine import SealEngine, SovereignSeal

__all__ = [
    "Federation", "Confederation", "League", "Club", "Coder", "CraftDomain",
    "License", "LicenseLevel", "Draft", "Transfer", "Calendar", "Match",
    "MatchKind", "MatchResult", "Arbitration", "ArbiterDecision", "Ranking",
    "MatchCore", "MatchEngine", "RuleEngine", "SealEngine", "SovereignSeal",
]
