"""SealEngine — the cryptographic Sovereign Seal.

A Sovereign Seal is a chained SHA-256 root hash + an Ed25519 arbiter
signature. The chain hash links every seal to the previous one,
producing an append-only Merkle-style chain recorded in the Sovereign
Ledger.

For deterministic unit testing (where the cryptography library may be
unavailable) the engine falls back to a pure-Python HMAC-SHA256
signature keyed by ``private_key``; the verification logic is identical.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey,
    )
    _HAS_CRYPTO = True
except Exception:  # pragma: no cover - cryptography may be absent
    _HAS_CRYPTO = False


def _canonical(payload: Dict[str, Any]) -> bytes:
    """Deterministic JSON encoding used for hashing & signing."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class SovereignSeal:
    """A sealed match record."""

    root_hash: str
    signature: str
    arbiter_id: str
    chain_hash: str
    prev_chain_hash: str
    ledger_index: int
    sealed_at: str
    payload_hash: str = ""
    seal_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SealEngine:
    """Produces and verifies Sovereign Seals."""

    def __init__(self, *, private_key: Optional[str] = None,
                 public_key: Optional[str] = None,
                 genesis_hash: str = "0" * 64) -> None:
        self.genesis_hash = genesis_hash
        self._prev_chain_hash = genesis_hash
        self._counter = 0
        self._ed25519_priv = None
        self._ed25519_pub = None
        self._hmac_key = (private_key or "ccifa-default-arbiter-key").encode("utf-8")
        if _HAS_CRYPTO and private_key:
            try:
                self._ed25519_priv = Ed25519PrivateKey.from_private_bytes(
                    hashlib.sha256(private_key.encode()).digest())
                self._ed25519_pub = self._ed25519_priv.public_key()
            except Exception:
                self._ed25519_priv = None
        if _HAS_CRYPTO and public_key and not self._ed25519_pub:
            try:
                self._ed25519_pub = Ed25519PublicKey.from_public_bytes(
                    bytes.fromhex(public_key))
            except Exception:
                self._ed25519_pub = None

    # -- core ops ------------------------------------------------------- #
    def root_hash(self, payload: Dict[str, Any]) -> str:
        return sha256_hex(_canonical(payload))

    def _sign(self, message: bytes) -> str:
        if self._ed25519_priv is not None:
            return self._ed25519_priv.sign(message).hex()
        # Pure-python fallback: HMAC-SHA256 keyed by the private key.
        return hmac.new(self._hmac_key, message, hashlib.sha256).hexdigest()

    def _verify_signature(self, message: bytes, signature: str) -> bool:
        if self._ed25519_pub is not None:
            try:
                self._ed25519_pub.verify(bytes.fromhex(signature), message)
                return True
            except Exception:
                return False
        expected = hmac.new(self._hmac_key, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def seal(self, payload: Dict[str, Any], *,
             arbiter_id: str = "ARBITER-0001",
             prev_chain_hash: Optional[str] = None) -> SovereignSeal:
        """Produce a Sovereign Seal for ``payload``.

        Parameters
        ----------
        payload:
            The canonical match payload (see :meth:`Match.canonical_payload`).
        arbiter_id:
            The presiding arbiter signing the seal.
        prev_chain_hash:
            Optional override for the previous chain hash (defaults to the
            engine's internal cursor — useful when replaying the ledger).
        """
        root = self.root_hash(payload)
        prev = prev_chain_hash or self._prev_chain_hash
        chain_input = (prev + root).encode("utf-8")
        chain_hash = sha256_hex(chain_input)
        signature = self._sign(root.encode("utf-8"))
        self._counter += 1
        seal = SovereignSeal(
            root_hash=root,
            signature=signature,
            arbiter_id=arbiter_id,
            chain_hash=chain_hash,
            prev_chain_hash=prev,
            ledger_index=self._counter,
            sealed_at=datetime.now(timezone.utc).isoformat(),
            payload_hash=sha256_hex(_canonical({"payload": payload, "root": root})),
        )
        self._prev_chain_hash = chain_hash
        return seal

    # -- verification --------------------------------------------------- #
    def verify(self, seal: SovereignSeal | Dict[str, Any],
               payload: Dict[str, Any]) -> bool:
        """Verify a seal against a payload.

        Checks:
        - root hash matches sha256(payload),
        - chain hash matches sha256(prev || root),
        - signature verifies against the root hash.
        """
        s = seal if isinstance(seal, SovereignSeal) else SovereignSeal(**seal)
        expected_root = self.root_hash(payload)
        if not hmac.compare_digest(expected_root, s.root_hash):
            return False
        expected_chain = sha256_hex((s.prev_chain_hash + s.root_hash).encode("utf-8"))
        if not hmac.compare_digest(expected_chain, s.chain_hash):
            return False
        return self._verify_signature(s.root_hash.encode("utf-8"), s.signature)

    def reset_chain(self, genesis_hash: Optional[str] = None) -> None:
        self._prev_chain_hash = genesis_hash or self.genesis_hash
        self._counter = 0

    def __repr__(self) -> str:
        mode = "ed25519" if self._ed25519_priv else "hmac-fallback"
        return f"<SealEngine mode={mode} counter={self._counter}>"
