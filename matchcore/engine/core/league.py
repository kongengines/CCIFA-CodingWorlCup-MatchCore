"""Leagues — annual competitions with calendars and rankings.

A league is a season-long competition. Each season has its own calendar
(round-robin or bracket), a live ranking and a set of played matches.
"""

from __future__ import annotations

import itertools
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from matchcore.engine.core.calendar import Calendar
from matchcore.engine.core.match import Match, MatchKind, MatchResult
from matchcore.engine.core.ranking import Ranking


class League:
    """A CCIFA league."""

    def __init__(self, league_id: str, name: str, *,
                 confederation_code: str = "EU",
                 kind: str = "national",
                 points_win: int = 3, points_draw: int = 1,
                 points_loss: int = 0) -> None:
        self.id = league_id
        self.name = name
        self.confederation_code = confederation_code
        self.kind = kind  # national | continental | worldcup
        self.points = {"W": points_win, "D": points_draw, "L": points_loss}
        self.clubs: List[str] = []
        self.season: Optional[int] = None
        self.calendar: Optional[Calendar] = None
        self.ranking = Ranking()

    # -- season lifecycle ---------------------------------------------- #
    def start_season(self, season: int, *, start_date: Optional[date] = None) -> Calendar:
        """Generate a round-robin calendar for the registered clubs."""
        if len(self.clubs) < 2:
            raise ValueError("Need at least 2 clubs to start a season")
        self.season = season
        self.calendar = self.generate_calendar(start_date or date(season, 1, 15))
        return self.calendar

    def generate_calendar(self, start_date: date) -> Calendar:
        """Round-robin double-leg calendar (home & away)."""
        clubs = list(self.clubs)
        if len(clubs) % 2 != 0:
            clubs.append("BYE")
        n = len(clubs)
        rounds = n - 1
        half = n // 2
        matches: List[Match] = []
        cur = start_date
        for r in range(rounds):
            for i in range(half):
                home = clubs[i]
                away = clubs[n - 1 - i]
                if home != "BYE" and away != "BYE":
                    matches.append(Match(
                        match_id=f"{self.id}-S{self.season}-R{r+1}-{i+1}",
                        home_id=home, away_id=away,
                        kind=MatchKind.OFFICIAL if self.kind != "friendly" else MatchKind.FRIENDLY,
                        scheduled_at=datetime.combine(cur, datetime.min.time(), tzinfo=timezone.utc),
                    ))
                    matches.append(Match(
                        match_id=f"{self.id}-S{self.season}-R{rounds+r+1}-{i+1}",
                        home_id=away, away_id=home,
                        kind=MatchKind.OFFICIAL if self.kind != "friendly" else MatchKind.FRIENDLY,
                        scheduled_at=datetime.combine(cur + timedelta(weeks=rounds), datetime.min.time(), tzinfo=timezone.utc),
                    ))
            # rotate (except first)
            clubs = [clubs[0]] + [clubs[-1]] + clubs[1:-1]
            cur += timedelta(weeks=1)
        self.calendar = Calendar(matches=matches)
        return self.calendar

    def register_club(self, club_id: str) -> None:
        if club_id not in self.clubs:
            self.clubs.append(club_id)

    # -- matches -------------------------------------------------------- #
    def play_match(self, match: Match, result: MatchResult) -> None:
        """Apply a finished match result to the ranking."""
        if not match.is_finished():
            raise ValueError("Match not finished")
        home_pts = away_pts = 0
        if result.home_score > result.away_score:
            home_pts = self.points["W"]; away_pts = self.points["L"]
            home_res, away_res = "W", "L"
        elif result.home_score < result.away_score:
            away_pts = self.points["W"]; home_pts = self.points["L"]
            home_res, away_res = "L", "W"
        else:
            home_pts = away_pts = self.points["D"]
            home_res = away_res = "D"
        self.ranking.update(match.home_id, home_pts, home_res,
                            gf=result.home_score, ga=result.away_score)
        self.ranking.update(match.away_id, away_pts, away_res,
                            gf=result.away_score, ga=result.home_score)

    def standings(self) -> List[Dict[str, Any]]:
        return self.ranking.to_dict()

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "confederation_code": self.confederation_code,
            "kind": self.kind,
            "clubs": list(self.clubs),
            "season": self.season,
            "points": dict(self.points),
            "calendar": self.calendar.to_dict() if self.calendar else None,
            "ranking": self.ranking.to_dict(),
        }

    def __repr__(self) -> str:
        return f"<League {self.id} {self.kind}>"
