"""The annual CCIFA draft.

Each season, eligible amateur/semi coders enter the draft. The draft
order is computed from the reverse of the previous season's ranking
(weakest club picks first). Each club picks one coder per round.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from matchcore.engine.core.coder import Coder


class Draft:
    """An annual CCIFA draft."""

    def __init__(self, draft_id: str, season: int) -> None:
        self.id = draft_id
        self.season = season
        self.order: List[str] = []          # club ids, picking order
        self.rounds: int = 1
        self.eligible: List[Coder] = []
        self.picks: List[Dict[str, Any]] = []
        self.created_at = datetime.now(timezone.utc)

    # -- preparation ---------------------------------------------------- #
    def set_eligible(self, coders: List[Coder]) -> None:
        self.eligible = list(coders)

    def compute_order(self, previous_ranking: List[Dict[str, Any]]) -> List[str]:
        """Draft order = reverse of the previous season's standings."""
        self.order = [row["club_id"] for row in sorted(previous_ranking, key=lambda r: r["points"])]
        return self.order

    # -- picking -------------------------------------------------------- #
    def pick(self, club_id: str, coder_id: str) -> Dict[str, Any]:
        if club_id not in self.order:
            raise ValueError(f"Club {club_id} not in draft order")
        coder = next((c for c in self.eligible if c.id == coder_id), None)
        if coder is None:
            raise ValueError(f"Coder {coder_id} not eligible for draft {self.id}")
        if any(p["coder_id"] == coder_id for p in self.picks):
            raise ValueError(f"Coder {coder_id} already picked")
        pick_record = {
            "draft_id": self.id,
            "season": self.season,
            "club_id": club_id,
            "coder_id": coder_id,
            "round": len(self.picks) // max(1, len(self.order)) + 1,
            "pick_number": len(self.picks) + 1,
            "picked_at": datetime.now(timezone.utc).isoformat(),
        }
        self.picks.append(pick_record)
        self.eligible = [c for c in self.eligible if c.id != coder_id]
        return pick_record

    def next_picker(self) -> Optional[str]:
        picked_clubs = {p["club_id"] for p in self.picks}
        for cid in self.order:
            if cid not in picked_clubs:
                return cid
        return None

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "season": self.season,
            "rounds": self.rounds,
            "order": list(self.order),
            "eligible": [c.id for c in self.eligible],
            "picks": list(self.picks),
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Draft {self.id} season={self.season} picks={len(self.picks)}>"
