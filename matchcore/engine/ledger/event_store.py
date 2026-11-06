"""EventStore — query layer over the SovereignLedger.

Provides high-level queries used by the dashboard and the API: by
type, by match, by arena, time-bounded scans and aggregate counts.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional

from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


class EventStore:
    """Query helpers around the Sovereign Ledger."""

    def __init__(self, ledger: SovereignLedger) -> None:
        self.ledger = ledger

    def all(self) -> List[Dict[str, Any]]:
        return list(self.ledger)

    def by_type(self, type_: str) -> List[Dict[str, Any]]:
        return [e for e in self.ledger if e.get("type") == type_]

    def by_match(self, match_id: str) -> List[Dict[str, Any]]:
        return [e for e in self.ledger
                if e.get("event", {}).get("match_id") == match_id]

    def by_arena(self, arena_node_id: str) -> List[Dict[str, Any]]:
        return [e for e in self.ledger
                if e.get("event", {}).get("arena_node_id") == arena_node_id]

    def count_by_type(self) -> Dict[str, int]:
        return Counter(e.get("type", "event") for e in self.ledger)

    def in_range(self, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for e in self.ledger:
            ts = e.get("appended_at")
            if not ts:
                continue
            try:
                t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                continue
            if start <= t <= end:
                out.append(e)
        return out

    def latest(self, n: int = 10) -> List[Dict[str, Any]]:
        return list(self.ledger)[-n:]

    def summary(self) -> Dict[str, Any]:
        return {
            "total": len(self.ledger),
            "by_type": self.count_by_type(),
            "verified": self.ledger.verify(),
            "last_hash": self.ledger.last_hash(),
        }
