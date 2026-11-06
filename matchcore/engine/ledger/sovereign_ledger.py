"""SovereignLedger — append-only, SHA-256-chained JSONL log.

Every event appended to the ledger is linked to the previous one by a
SHA-256 chain hash. The genesis hash is configurable (env
``SEAL_GENESIS_HASH``). Verification replays the whole log and checks
every link.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional


GENESIS_HASH = os.environ.get("SEAL_GENESIS_HASH", "0" * 64)


class SovereignLedger:
    """Append-only, chained, JSONL event log."""

    def __init__(self, path: str | os.PathLike = "matchcore/data/sovereign-ledger.jsonl",
                 *, genesis_hash: str = GENESIS_HASH) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()
        self.genesis_hash = genesis_hash
        self._entries: List[Dict[str, Any]] = self._load()

    # -- internal ------------------------------------------------------- #
    def _load(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        with self.path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    @staticmethod
    def _chain(prev: str, payload: Dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False).encode("utf-8")
        return hashlib.sha256((prev + hashlib.sha256(canonical).hexdigest()).encode()).hexdigest()

    # -- public API ----------------------------------------------------- #
    def append(self, event: Dict[str, Any]) -> Dict[str, Any]:
        prev = self._entries[-1]["chain_hash"] if self._entries else self.genesis_hash
        index = len(self._entries) + 1
        record = {
            "index": index,
            "prev_hash": prev,
            "chain_hash": "",  # filled below
            "event": event,
            "type": event.get("type", "event"),
            "appended_at": datetime.now(timezone.utc).isoformat(),
        }
        record["chain_hash"] = self._chain(prev, event)
        self._entries.append(record)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def last_hash(self) -> str:
        return self._entries[-1]["chain_hash"] if self._entries else self.genesis_hash

    def verify(self) -> bool:
        """Replay the chain from genesis; return True iff every link holds."""
        prev = self.genesis_hash
        for i, entry in enumerate(self._entries, 1):
            if entry["index"] != i:
                return False
            if entry["prev_hash"] != prev:
                return False
            expected = self._chain(prev, entry["event"])
            if entry["chain_hash"] != expected:
                return False
            prev = entry["chain_hash"]
        return True

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        return self._entries[idx]

    def query(self, *, type: Optional[str] = None,
              match_id: Optional[str] = None) -> List[Dict[str, Any]]:
        out = []
        for e in self._entries:
            if type and e.get("type") != type:
                continue
            if match_id and e["event"].get("match_id") != match_id:
                continue
            out.append(e)
        return out

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": str(self.path),
            "entries": len(self._entries),
            "genesis_hash": self.genesis_hash,
            "last_hash": self.last_hash(),
            "verified": self.verify(),
        }

    def __repr__(self) -> str:
        return f"<SovereignLedger {self.path} entries={len(self._entries)}>"
