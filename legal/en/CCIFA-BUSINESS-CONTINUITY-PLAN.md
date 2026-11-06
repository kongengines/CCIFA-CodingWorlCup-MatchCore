# CCIFA Business Continuity Plan

**Code & Craft International Federation Association (CCIFA)**

> Version v1.0 — English master text.

---

## 1. Purpose

This Business Continuity Plan (BCP) ensures that CCIFA can continue
to govern sport-coding and verify the Sovereign Ledger in the face
of disruption.

## 2. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| MatchCore outage | Medium | High | Hot standby, health-checks |
| Sovereign Ledger corruption | Low | Critical | SHA-256 chain, offsite backup |
| Arena node failure | Medium | High | Min 3 nodes per match |
| Arbiter key compromise | Low | Critical | HSM, key rotation |
| USB courier loss | Medium | Medium | Signed bundles, root hash |
| Cyber attack on dashboard | Medium | Medium | WAF, rate limiting |
| Loss of certified languages | Low | Medium | 11 locales, fallback to EN |

## 3. Governance

- The Executive Committee declares a continuity incident.
- The Ethics & Integrity Committee coordinates recovery.
- The Arbitration Committee rules on match validity post-incident.

## 4. Continuity Strategies

- **MatchCore**: blue/green deployment, automatic failover.
- **Sovereign Ledger**: append-only; nightly offsite backup; the
  genesis hash is published in 11 languages.
- **Arena**: minimum 3 nodes per match; if one fails, the match is
  voided and replayed.
- **Arbiter keys**: HSM-backed Ed25519; rotation every 2 years.
- **USB courier**: sworn courier, signed bundle, root hash verification.

## 5. Recovery Procedures

1. Detect (health check, alert, incident report).
2. Contain (isolate the failing component).
3. Recover (failover, replay from ledger, re-seal if needed).
4. Verify (full ledger verification via `POST /ledger/verify`).
5. Communicate (see the Communication Plan).

## 6. Communication Plan

- Internal: Executive Committee within 1 hour.
- Public: status-site update within 2 hours.
- Multi-language: announcements in all 11 Certified Languages.
- Post-mortem: published within 30 days, recorded in the Sovereign Ledger.

## 7. Testing

- Tabletop exercise quarterly.
- Full failover drill annually.
- Ledger verification drill semi-annually.

---

## CCIFA Certification Block

| Field | Value |
|------|-------|
| Document | CCIFA Business Continuity Plan |
| Language | English (master) |
| Version | v1.0 |
| Issued by | CCIFA Executive Committee |
| Certified languages | EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR |
| Seal | SHA-256(ccifa-legal-bcp) |
| Status | Certified |

> This document is certified in all 11 CCIFA Certified Languages. In the
> event of any inconsistency, the English master text shall prevail.

> **Sovereign Ledger reference**: this charter is anchored to the
> Sovereign Ledger by its root hash and may be verified at any time via
> the MatchCore REST endpoint `GET /seals/{root}`.

Certified by the **CCIFA Executive Committee** on behalf of the Code &
Craft International Federation Association.
