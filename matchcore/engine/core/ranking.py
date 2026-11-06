"""Rankings — live standings for a league or confederation."""

from __future__ import annotations

from typing import Any, Dict, List


class RankingRow:
    """A single row in a ranking table."""

    __slots__ = ("club_id", "played", "wins", "draws", "losses",
                 "goals_for", "goals_against", "points")

    def __init__(self, club_id: str) -> None:
        self.club_id = club_id
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    def to_dict(self) -> Dict[str, Any]:
        return {
            "club_id": self.club_id,
            "played": self.played,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "goals_for": self.goals_for,
            "goals_against": self.goals_against,
            "goal_difference": self.goal_difference,
            "points": self.points,
        }


class Ranking:
    """A live ranking table."""

    def __init__(self) -> None:
        self.rows: Dict[str, RankingRow] = {}

    def _row(self, club_id: str) -> RankingRow:
        if club_id not in self.rows:
            self.rows[club_id] = RankingRow(club_id)
        return self.rows[club_id]

    def update(self, club_id: str, points: int, result: str, *,
               gf: int = 0, ga: int = 0) -> None:
        row = self._row(club_id)
        row.played += 1
        row.points += points
        row.goals_for += gf
        row.goals_against += ga
        if result == "W":
            row.wins += 1
        elif result == "D":
            row.draws += 1
        elif result == "L":
            row.losses += 1

    def top(self, n: int = 10) -> List[RankingRow]:
        return sorted(self.rows.values(),
                      key=lambda r: (r.points, r.goal_difference, r.goals_for),
                      reverse=True)[:n]

    def to_dict(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in
                sorted(self.rows.values(),
                       key=lambda r: (r.points, r.goal_difference, r.goals_for),
                       reverse=True)]

    def __repr__(self) -> str:
        return f"<Ranking {len(self.rows)} clubs>"
