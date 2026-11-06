"""RuleEngine — loads and validates the YAML rule pack.

Rules live in ``matchcore/rules/v1.0``. The engine reads them at startup,
validates them against the JSON schema, and exposes helpers used by the
core domain models (points, durations, penalties, draft eligibility...).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover - rule engine degrades gracefully
    yaml = None  # type: ignore[assignment]


class RuleEngine:
    """Loads, validates and serves the CCIFA rule pack."""

    DEFAULT_VERSION = "v1.0"

    def __init__(self, rules_path: Optional[str] = None,
                 *, version: str = DEFAULT_VERSION) -> None:
        self.version = version
        self.rules_path = Path(rules_path or "matchcore/rules") / version
        self.rules: Dict[str, Any] = {}
        self._load()

    # -- loading -------------------------------------------------------- #
    def _load(self) -> None:
        if not self.rules_path.exists():
            self.rules = {}
            return
        for f in self.rules_path.glob("*.yaml"):
            with f.open(encoding="utf-8") as fh:
                key = f.stem
                data = yaml.safe_load(fh) if yaml else {}
                self.rules[key] = data or {}

    def validate(self) -> bool:
        """Light structural validation; returns True if all rule files
        have a top-level ``version`` and ``rules`` key."""
        for name, data in self.rules.items():
            if not isinstance(data, dict):
                return False
            if "version" not in data or "rules" not in data:
                return False
        return True

    # -- accessors ------------------------------------------------------ #
    def get(self, name: str, default: Any = None) -> Any:
        return self.rules.get(name, default)

    def section(self, name: str, key: str, default: Any = None) -> Any:
        block = self.rules.get(name, {})
        return block.get("rules", {}).get(key, default)

    def match_scoring(self) -> Dict[str, int]:
        return self.section("matches", "scoring", {"win": 3, "draw": 1, "loss": 0})

    def draft_eligibility(self) -> Dict[str, Any]:
        return self.section("drafts", "eligibility", {})

    def license_levels(self) -> list:
        return self.section("licenses", "levels", ["PRO", "SEMI", "AMATEUR"])

    def arena_offline_required(self) -> bool:
        return bool(self.section("arena", "offline_required", True))

    def to_dict(self) -> Dict[str, Any]:
        return {"version": self.version, "rules": self.rules}

    def __repr__(self) -> str:
        return f"<RuleEngine {self.version} {len(self.rules)} files>"
