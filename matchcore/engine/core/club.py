"""Clubs — the teams of sport-coding.

A club has a roster of coders, a budget, an optional sponsor and a set
of transfer-window operations. Clubs are the primary organisational
unit below leagues/confederations.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from matchcore.engine.core.coder import Coder


class Club:
    """A CCIFA-affiliated club."""

    def __init__(self, club_id: str, name: str, country: str, *,
                 budget: int = 0, sponsor: Optional[str] = None,
                 founded: int = 2020) -> None:
        self.id = club_id
        self.name = name
        self.country = country.upper()
        self.budget = budget
        self.sponsor = sponsor
        self.founded = founded
        self.roster: List[Coder] = []
        self.created_at = datetime.now(timezone.utc)

    # -- roster management ---------------------------------------------- #
    def sign(self, coder: Coder, *, salary: int = 0) -> Coder:
        """Sign a coder onto the roster."""
        if salary > self.budget:
            raise ValueError(f"Club {self.id} cannot afford salary {salary} (budget {self.budget})")
        if any(c.id == coder.id for c in self.roster):
            raise ValueError(f"Coder {coder.id} already on roster of {self.id}")
        self.budget -= salary
        if coder.license is not None:
            coder.sign_contract(coder.license, self.id)
        else:
            coder.club_id = self.id
        self.roster.append(coder)
        return coder

    def release(self, coder_id: str) -> Optional[Coder]:
        """Release a coder from the roster."""
        for i, c in enumerate(self.roster):
            if c.id == coder_id:
                self.roster.pop(i)
                c.release()
                return c
        return None

    def roster_by_craft(self, craft: str) -> List[Coder]:
        return [c for c in self.roster if c.craft.value == craft]

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "budget": self.budget,
            "sponsor": self.sponsor,
            "founded": self.founded,
            "roster_size": len(self.roster),
            "roster": [c.to_dict() for c in self.roster],
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Club {self.id} {self.name} ({len(self.roster)} coders)>"
