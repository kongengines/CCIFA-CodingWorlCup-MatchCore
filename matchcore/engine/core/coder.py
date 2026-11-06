"""Coders — the athletes of sport-coding.

Every coder holds exactly one CCIFA :class:`License`, belongs to at most
one club, and may be selected for a national team. Coders are split into
four craft domains.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from matchcore.engine.core.license import License, LicenseLevel


class CraftDomain(str, Enum):
    """The four certified craft domains of CCIFA."""

    CODER = "Coder"
    DESIGNER = "Designer"
    MAKER = "Maker"
    STRATEGIST = "Strategist"


class CoderStats:
    """Rolling competitive statistics for a coder."""

    __slots__ = ("matches", "wins", "draws", "losses", "points", "skill")

    def __init__(self, *, skill: int = 50) -> None:
        self.matches = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.points = 0
        self.skill = skill

    def record(self, result: str, points: int = 0) -> None:
        self.matches += 1
        self.points += points
        if result == "W":
            self.wins += 1
        elif result == "D":
            self.draws += 1
        elif result == "L":
            self.losses += 1

    def to_dict(self) -> Dict[str, Any]:
        return {s: getattr(self, s) for s in self.__slots__}


class Coder:
    """A registered CCIFA coder.

    Parameters
    ----------
    coder_id:
        Stable unique identifier.
    name:
        Display name.
    nationality:
        ISO-3 country code (e.g. ``FRA``).
    craft:
        :class:`CraftDomain`.
    skill:
        Initial skill rating 1-100.
    """

    def __init__(self, coder_id: str, name: str, nationality: str,
                 craft: CraftDomain | str = CraftDomain.CODER,
                 *, skill: int = 50) -> None:
        self.id = coder_id
        self.name = name
        self.nationality = nationality.upper()
        self.craft = CraftDomain(craft) if isinstance(craft, str) else craft
        self.license: Optional[License] = None
        self.club_id: Optional[str] = None
        self.national_team_caps: int = 0
        self.stats = CoderStats(skill=max(1, min(100, skill)))
        self.created_at = datetime.now(timezone.utc)

    # -- contracts ------------------------------------------------------ #
    def sign_contract(self, license_: License, club_id: str) -> None:
        """Sign with a club under a given license."""
        if license_.holder != self.id:
            raise ValueError("License holder mismatch")
        if license_.status.value != "ACTIVE":
            raise ValueError("License not active")
        self.license = license_
        self.club_id = club_id

    def release(self) -> None:
        """Release the coder from their current club (does not revoke license)."""
        self.club_id = None

    # -- eligibility ---------------------------------------------------- #
    def national_team_eligible(self) -> bool:
        """A coder is eligible for their national team if they hold a valid
        PRO or SEMI license and have not been capped for another nation."""
        if self.license is None or not self.license.validate():
            return False
        return self.license.level in (LicenseLevel.PRO, LicenseLevel.SEMI)

    def record_match(self, result: str, points: int = 0) -> None:
        self.stats.record(result, points)
        # Gently drift skill rating up on wins, down on losses.
        delta = {"W": 2, "D": 0, "L": -1}.get(result, 0)
        self.stats.skill = max(1, min(100, self.stats.skill + delta))

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "nationality": self.nationality,
            "craft": self.craft.value,
            "license": self.license.to_dict() if self.license else None,
            "club_id": self.club_id,
            "national_team_caps": self.national_team_caps,
            "stats": self.stats.to_dict(),
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Coder {self.id} {self.craft.value} skill={self.stats.skill}>"
