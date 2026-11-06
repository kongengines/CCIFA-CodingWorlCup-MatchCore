"""ArenaNode — executes an official match offline and seals the result."""

from __future__ import annotations

import os
import socket
import time
from typing import Any, Dict, Optional

from matchcore.engine.core.match import Match
from matchcore.engine.core.seal_engine import SealEngine
from matchcore.engine.ledger.sovereign_ledger import SovereignLedger


class ArenaNode:
    """A sovereign arena node.

    The node asserts that no network is reachable, runs the match,
    produces the Sovereign Seal and exports the ledger entry to
    physical media (USB).
    """

    def __init__(self, node_id: str, *, seal_engine: SealEngine,
                 ledger: SovereignLedger,
                 usb_mount: Optional[str] = None) -> None:
        self.node_id = node_id
        self.seal_engine = seal_engine
        self.ledger = ledger
        self.usb_mount = usb_mount or os.environ.get("ARENA_USB_MOUNT", "/media/sovereign")
        self.matches_run = 0

    # -- assertions ----------------------------------------------------- #
    @staticmethod
    def assert_network_disabled() -> bool:
        """Return True if no external TCP connection can be established."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect(("8.8.8.8", 53))
            s.close()
            return False  # network is REACHABLE — failure!
        except OSError:
            return True  # network is properly disabled

    # -- execution ------------------------------------------------------ #
    def run_match(self, match: Match, home_score: int, away_score: int,
                  *, arbiter_id: str) -> Dict[str, Any]:
        if match.kind.value != "OFFICIAL":
            raise ValueError("ArenaNode only runs OFFICIAL matches")
        if not self.assert_network_disabled():
            raise RuntimeError("ARENA_NETWORK_ASSERTION_FAILED: network reachable")
        match.arena_node_id = self.node_id
        match.arbiter_id = arbiter_id
        match.start()
        # simulate arbitration time
        time.sleep(0.01)
        match.finish(home_score, away_score)
        seal = self.seal_engine.seal(match.canonical_payload(), arbiter_id=arbiter_id)
        match.attach_seal(seal)
        event = {
            "type": "match.official.sealed",
            "match_id": match.id,
            "home_id": match.home_id,
            "away_id": match.away_id,
            "arena_node_id": self.node_id,
            "arbiter_id": arbiter_id,
            "result": match.result.to_dict() if match.result else None,
            "seal": seal.to_dict(),
            "ts": time.time(),
        }
        self.ledger.append(event)
        self.matches_run += 1
        return event

    def __repr__(self) -> str:
        return f"<ArenaNode {self.node_id} matches_run={self.matches_run}>"
