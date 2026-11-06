# CCIFA Incident Playbook

**Code & Craft International Federation Association (CCIFA)**

> Version v1.0 — English master text.

---

## 1. Severity Levels

| Severity | Definition | Response time |
|----------|-----------|---------------|
| SEV-1 | Sovereign Ledger corrupted or arbiter key compromised | 15 min |
| SEV-2 | MatchCore down, arena node offline during a match | 30 min |
| SEV-3 | Dashboard degraded, partial API failure | 2 h |
| SEV-4 | Cosmetic, single-language defect | 1 business day |

## 2. Roles

- **Incident Commander** — Executive Committee member on call.
- **Technical Lead** — MatchCore maintainer.
- **Arbiter Liaison** — Arbitration Committee member.
- **Communications Lead** — status-site owner.

## 3. Runbook — MatchCore Failure

1. Confirm via `/health` (200 + `ledger_verified: true`).
2. If down, failover to the hot standby.
3. Verify the Sovereign Ledger (`POST /ledger/verify`).
4. If ledger fails, declare SEV-1 and start the Ledger Runbook.

## 4. Runbook — Sovereign Ledger Failure

1. Stop all writes immediately.
2. Snapshot the JSONL file.
3. Replay verification from the last known-good hash.
4. Re-seal any unsealed matches via the ArenaNode.
5. Publish the new genesis hash in 11 languages.

## 5. Runbook — Arena Node Failure

1. The presiding arbiter voids the match.
2. The match is replayed on a backup node.
3. The original (voided) record is annotated in the ledger.
4. The sealed replay supersedes the void.

## 6. Runbook — Arbiter Key Compromise

1. Revoke the arbiter accreditation.
2. Rotate the HSM key.
3. Re-seal any matches signed by the compromised key.
4. Publish a security advisory in 11 languages.

## 7. Post-Incident

- Blameless post-mortem within 7 days.
- Action items tracked in the Sovereign Ledger.
- Quarterly review by the Ethics & Integrity Committee.

---

## CCIFA Certification Block

| Field | Value |
|------|-------|
| Document | CCIFA Incident Playbook |
| Language | English (master) |
| Version | v1.0 |
| Issued by | CCIFA Executive Committee |
| Certified languages | EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR |
| Seal | SHA-256(ccifa-legal-incident) |
| Status | Certified |

> This document is certified in all 11 CCIFA Certified Languages. In the
> event of any inconsistency, the English master text shall prevail.

> **Sovereign Ledger reference**: this charter is anchored to the
> Sovereign Ledger by its root hash and may be verified at any time via
> the MatchCore REST endpoint `GET /seals/{root}`.

Certified by the **CCIFA Executive Committee** on behalf of the Code &
Craft International Federation Association.
