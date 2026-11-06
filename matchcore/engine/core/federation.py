"""The CCIFA federation.

The federation is the top of the sport-coding pyramid. It owns the
organigram, the standing committees and the five continental
confederations. It is the only entity that can issue licenses and
accredit arbiters.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from matchcore.engine.core.confederation import CONFEDERATION_CODES, Confederation
from matchcore.engine.core.license import License, LicenseLevel


COMMITTEES = (
    "Executive Committee",
    "Sport-Coding Committee",
    "Arbitration Committee",
    "Ethics & Integrity Committee",
)


class Organigram:
    """The CCIFA organigram (president + committees)."""

    def __init__(self, president: str = "Dr. Ada Lovelace-Coding") -> None:
        self.president = president
        self.committees: Dict[str, List[str]] = {c: [] for c in COMMITTEES}

    def add_member(self, committee: str, member: str) -> None:
        if committee not in self.committees:
            raise ValueError(f"Unknown committee: {committee}")
        self.committees[committee].append(member)

    def to_dict(self) -> Dict[str, Any]:
        return {"president": self.president, "committees": dict(self.committees)}


class Federation:
    """The CCIFA federation."""

    def __init__(self, *, president: str = "Dr. Ada Lovelace-Coding") -> None:
        self.name = "Code & Craft International Federation Association"
        self.short_name = "CCIFA"
        self.organigram = Organigram(president)
        self.confederations: Dict[str, Confederation] = {}
        self.licensed_coders: Dict[str, License] = {}
        self.accredited_arbiters: List[str] = []
        self.created_at = datetime.now(timezone.utc)
        self._seed_confederations()

    def _seed_confederations(self) -> None:
        defaults = {
            "AF": ("African Confederation", "Africa"),
            "AM": ("Americas Confederation", "Americas"),
            "AS": ("Asian Confederation", "Asia"),
            "EU": ("European Confederation", "Europe"),
            "OC": ("Oceanian Confederation", "Oceania"),
        }
        for code, (name, region) in defaults.items():
            self.confederations[code] = Confederation(code, name, region=region)

    # -- confederations ------------------------------------------------- #
    def add_confederation(self, confederation: Confederation) -> Confederation:
        self.confederations[confederation.code] = confederation
        return confederation

    def get_confederation(self, code: str) -> Optional[Confederation]:
        return self.confederations.get(code.upper())

    def all_confederations(self) -> List[Confederation]:
        return list(self.confederations.values())

    def all_leagues(self) -> List[str]:
        leagues: List[str] = []
        for c in self.confederations.values():
            leagues.extend(c.national_leagues)
            leagues.extend(c.continental_leagues)
        return leagues

    # -- licensing ------------------------------------------------------ #
    def issue_license(self, level: LicenseLevel | str, coder_id: str,
                      season: int) -> License:
        lic = License(level, coder_id, season).issue()
        self.licensed_coders[lic.code] = lic
        return lic

    def revoke_license(self, code: str, reason: str) -> Optional[License]:
        lic = self.licensed_coders.get(code)
        if lic is not None:
            lic.revoke(reason)
        return lic

    def accredit_arbiter(self, arbiter_id: str) -> None:
        if arbiter_id not in self.accredited_arbiters:
            self.accredited_arbiters.append(arbiter_id)

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "short_name": self.short_name,
            "organigram": self.organigram.to_dict(),
            "confederations": {k: v.to_dict() for k, v in self.confederations.items()},
            "licensed_coders": len(self.licensed_coders),
            "accredited_arbiters": list(self.accredited_arbiters),
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Federation {self.short_name} ({len(self.confederations)} confederations)>"


__all__ = ["Federation", "Organigram", "COMMITTEES", "CONFEDERATION_CODES"]
