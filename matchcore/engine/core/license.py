"""Coder licenses issued by CCIFA.

A license is the sovereign permit that lets a coder compete in official
matches. Three levels exist: PRO, SEMI and AMATEUR. Licenses can be
issued, validated and revoked.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict


class LicenseLevel(str, Enum):
    """The three certified CCIFA license levels."""

    PRO = "PRO"
    SEMI = "SEMI"
    AMATEUR = "AMATEUR"

    @property
    def salary_cap(self) -> int:
        """Annual salary cap (CCIFA units) for the level."""
        return {LicenseLevel.PRO: 5_000_000, LicenseLevel.SEMI: 750_000,
                LicenseLevel.AMATEUR: 0}[self]

    @property
    def can_play_official(self) -> bool:
        return self in (LicenseLevel.PRO, LicenseLevel.SEMI)


class LicenseStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class License:
    """A CCIFA coder license.

    Attributes
    ----------
    code:
        Human-readable license code, e.g. ``CCIFA-PRO-2026-000123``.
    level:
        One of ``PRO``, ``SEMI``, ``AMATEUR``.
    holder:
        Coder identifier that owns the license.
    issued_at / expires_at:
        Validity window.
    status:
        ``PENDING`` -> ``ACTIVE`` -> ``REVOKED`` / ``EXPIRED``.
    """

    def __init__(self, level: LicenseLevel | str, holder: str,
                 season: int, *, expires_at: datetime | None = None) -> None:
        self.level = LicenseLevel(level) if isinstance(level, str) else level
        self.holder = holder
        self.season = season
        self.code = f"CCIFA-{self.level.value}-{season}-{uuid.uuid4().hex[:6].upper()}"
        self.issued_at = datetime.now(timezone.utc)
        self.expires_at = expires_at or datetime(season + 1, 8, 31, tzinfo=timezone.utc)
        self.status: LicenseStatus = LicenseStatus.PENDING
        self.revocation_reason: str | None = None

    # -- lifecycle ------------------------------------------------------ #
    def issue(self) -> "License":
        """Activate the license (called by the federation registrar)."""
        if self.status is not LicenseStatus.PENDING:
            raise ValueError(f"License {self.code} already activated")
        self.status = LicenseStatus.ACTIVE
        return self

    def validate(self, *, now: datetime | None = None) -> bool:
        """Return True if the license is currently valid for an official match."""
        now = now or datetime.now(timezone.utc)
        if self.status is not LicenseStatus.ACTIVE:
            return False
        if now > self.expires_at:
            self.status = LicenseStatus.EXPIRED
            return False
        return self.level.can_play_official

    def revoke(self, reason: str) -> "License":
        if self.status is LicenseStatus.REVOKED:
            return self
        self.status = LicenseStatus.REVOKED
        self.revocation_reason = reason
        return self

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "level": self.level.value,
            "holder": self.holder,
            "season": self.season,
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "status": self.status.value,
            "revocation_reason": self.revocation_reason,
            "salary_cap": self.level.salary_cap,
        }

    def __repr__(self) -> str:
        return f"<License {self.code} {self.status.value}>"
