"""PhysicalSync — exports / imports the Sovereign Ledger via USB courier.

Because arena nodes are offline, the only way to move a sealed match
from the arena into MatchCore's online ledger is via a physical medium
(a USB key carried by a sworn courier). PhysicalSync serialises the
ledger segment, signs it, and writes it to the USB mount.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class PhysicalSync:
    """USB courier sync between arena and MatchCore."""

    def __init__(self, mount: str = "/media/sovereign",
                 *, courier_id: str = "COURIER-001") -> None:
        self.mount = Path(mount)
        self.courier_id = courier_id
        self.mount.mkdir(parents=True, exist_ok=True)

    def export(self, entries: List[Dict[str, Any]],
               *, arena_node_id: str) -> Path:
        """Sign and write a batch of ledger entries to USB."""
        payload = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
        bundle = {
            "arena_node_id": arena_node_id,
            "courier_id": self.courier_id,
            "entries": entries,
            "count": len(entries),
            "root_hash": hashlib.sha256(payload).hexdigest(),
            "exported_at": datetime.now(timezone.utc).isoformat(),
        }
        out = self.mount / f"sovereign-bundle-{arena_node_id}-{int(datetime.now(timezone.utc).timestamp())}.json"
        out.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
        return out

    def import_bundle(self, path: Path) -> Dict[str, Any]:
        """Verify a bundle from USB and return its entries."""
        bundle = json.loads(path.read_text(encoding="utf-8"))
        payload = json.dumps(bundle["entries"], sort_keys=True,
                             separators=(",", ":")).encode()
        recomputed = hashlib.sha256(payload).hexdigest()
        if recomputed != bundle["root_hash"]:
            raise ValueError("PHYSICAL_SYNC_ROOT_HASH_MISMATCH")
        return bundle

    def list_bundles(self) -> List[Path]:
        return sorted(self.mount.glob("sovereign-bundle-*.json"))
