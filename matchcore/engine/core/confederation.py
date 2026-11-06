"""Continental confederations.

CCIFA recognises five continental confederations, each one a regional
federation that aggregates national leagues, continental leagues and
the national teams eligible to qualify for the World Cup.
"""

from __future__ import annotations

from typing import Any, Dict, List

CONFEDERATION_CODES = ("AF", "AM", "AS", "EU", "OC")


class Confederation:
    """A continental confederation.

    Parameters
    ----------
    code:
        Two-letter confederation code (``AF``, ``AM``, ``AS``, ``EU``, ``OC``).
    name:
        Human-readable name (e.g. ``African Confederation``).
    """

    def __init__(self, code: str, name: str, *, region: str = "") -> None:
        if code not in CONFEDERATION_CODES:
            raise ValueError(f"Unknown confederation code: {code}")
        self.code = code
        self.name = name
        self.region = region or name
        self.national_leagues: List[str] = []
        self.continental_leagues: List[str] = []
        self.national_teams: List[str] = []

    # -- aggregation ---------------------------------------------------- #
    def add_national_league(self, league_id: str) -> None:
        if league_id not in self.national_leagues:
            self.national_leagues.append(league_id)

    def add_continental_league(self, league_id: str) -> None:
        if league_id not in self.continental_leagues:
            self.continental_leagues.append(league_id)

    def add_national_team(self, country: str) -> None:
        country = country.upper()
        if country not in self.national_teams:
            self.national_teams.append(country)

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "region": self.region,
            "national_leagues": list(self.national_leagues),
            "continental_leagues": list(self.continental_leagues),
            "national_teams": list(self.national_teams),
        }

    def __repr__(self) -> str:
        return f"<Confederation {self.code} {self.name}>"
