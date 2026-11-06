"""Transfers — the movement of coders between clubs.

Transfers only happen inside official windows and require validation by
both clubs, the coder, a medical (skill) check and the federation's
sign-off.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class TransferStatus(str, Enum):
    PROPOSED = "PROPOSED"
    VALIDATED = "VALIDATED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class TransferWindow:
    """A transfer window (open/closed date range)."""

    def __init__(self, opens_at: datetime, closes_at: datetime) -> None:
        self.opens_at = opens_at
        self.closes_at = closes_at

    def is_open(self, *, now: Optional[datetime] = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.opens_at <= now <= self.closes_at

    def to_dict(self) -> Dict[str, Any]:
        return {"opens_at": self.opens_at.isoformat(),
                "closes_at": self.closes_at.isoformat()}


class Transfer:
    """A single coder transfer between two clubs."""

    def __init__(self, transfer_id: str, coder_id: str,
                 from_club_id: str, to_club_id: str, *,
                 fee: int = 0,
                 window: Optional[TransferWindow] = None) -> None:
        self.id = transfer_id
        self.coder_id = coder_id
        self.from_club_id = from_club_id
        self.to_club_id = to_club_id
        self.fee = fee
        self.window = window
        self.status = TransferStatus.PROPOSED
        self.signatures: Dict[str, str] = {}
        self.medical_passed = False
        self.federation_approved = False
        self.created_at = datetime.now(timezone.utc)
        self.completed_at: Optional[datetime] = None

    # -- validation ----------------------------------------------------- #
    def sign(self, party: str, signature: str) -> None:
        self.signatures[party] = signature

    def pass_medical(self) -> None:
        self.medical_passed = True

    def federation_signoff(self) -> None:
        self.federation_approved = True

    def validate(self, *, now: Optional[datetime] = None) -> bool:
        """Validate that all parties signed, medical passed, federation approved
        and the transfer window is open."""
        if self.window is not None and not self.window.is_open(now=now):
            return False
        required = {"from_club", "to_club", "coder"}
        if not required.issubset(self.signatures.keys()):
            return False
        if not self.medical_passed:
            return False
        if not self.federation_approved:
            return False
        self.status = TransferStatus.VALIDATED
        return True

    def complete(self) -> "Transfer":
        if self.status is not TransferStatus.VALIDATED:
            raise ValueError("Transfer must be validated before completion")
        self.status = TransferStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        return self

    def reject(self, reason: str) -> "Transfer":
        self.status = TransferStatus.REJECTED
        self.signatures["rejection_reason"] = reason
        return self

    # -- serialisation -------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "coder_id": self.coder_id,
            "from_club_id": self.from_club_id,
            "to_club_id": self.to_club_id,
            "fee": self.fee,
            "status": self.status.value,
            "signatures": dict(self.signatures),
            "medical_passed": self.medical_passed,
            "federation_approved": self.federation_approved,
            "window": self.window.to_dict() if self.window else None,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    def __repr__(self) -> str:
        return f"<Transfer {self.id} {self.status.value}>"


__all__ = ["Transfer", "TransferWindow", "TransferStatus"]
