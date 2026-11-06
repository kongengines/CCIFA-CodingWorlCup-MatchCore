# CCIFA Official Regulations

**Code & Craft International Federation Association (CCIFA)**
**Coding World Cup — Sovereign Sport-Coding Statutes**

> Version v1.0 — English master text. Certified in 11 languages.

---

## Preamble

The Code & Craft International Federation Association ("CCIFA") is the
international federation governing the Coding World Cup, a quadrennial
sport-coding competition organised among the five continental
confederations and their affiliated national federations.

MatchCore is the living, online, sovereign engine that governs every
dimension of sport-coding life: federations, confederations, leagues,
clubs, coders, drafts, licenses, transfers, rankings, calendars,
arbitration, matches, and the World Cup.

Only **official matches** are played **100% offline** in sovereign
arenas. Every official match is sealed by a chained SHA-256 hash and
an Ed25519 arbiter signature (the "Sovereign Seal") and is recorded
immutably in the Sovereign Ledger.

---

## Article 1 — Definitions

1.1 **CCIFA**: the Code & Craft International Federation Association.

1.2 **MatchCore**: the sovereign engine of CCIFA, including its rule
   pack, REST API, CLI, dashboard and the Sovereign Ledger.

1.3 **Confederation**: one of the five continental bodies — African
   (AF), Americas (AM), Asian (AS), European (EU) and Oceanian (OC).

1.4 **League**: an annual competition (national, continental or the
   World Cup) with a calendar and a ranking.

1.5 **Club**: an affiliated sport-coding club with a roster, budget
   and optional sponsor.

1.6 **Coder**: a licensed athlete of one of the four craft domains —
   Coder, Designer, Maker, Strategist.

1.7 **Official Match**: a match played 100% offline in a sovereign
   arena, sealed and recorded in the Sovereign Ledger.

1.8 **Sovereign Seal**: the cryptographic record comprising a chained
   SHA-256 root hash and an Ed25519 arbiter signature.

1.9 **Sovereign Ledger**: the append-only, SHA-256-chained JSONL log
   of every CCIFA event.

1.10 **Certified Languages**: EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR.

---

## Article 2 — Federation Structure

2.1 CCIFA is composed of a President, three Vice-Presidents and four
    standing committees: the Executive Committee, the Sport-Coding
    Committee, the Arbitration Committee and the Ethics & Integrity
    Committee.

2.2 The President is elected for a renewable four-year term by the
    General Assembly.

2.3 The Executive Committee manages the day-to-day affairs of CCIFA.

2.4 The Sport-Coding Committee governs the sport-coding rule pack
    (matches, drafts, licenses, transfers, calendars, rankings).

2.5 The Arbitration Committee accredits arbiters and rules on appeals.

2.6 The Ethics & Integrity Committee enforces the Disciplinary Code.

2.7 The five confederations are autonomous in their internal affairs
    but bound by these Regulations.

---

## Article 3 — Licenses

3.1 Three license levels exist: **PRO**, **SEMI** and **AMATEUR**.

3.2 Only PRO and SEMI license holders may compete in official matches.

3.3 Licenses are issued for a season and expire on 31 August.

3.4 Licenses require federation sign-off, a medical (skill) check and
    an ethics screening.

3.5 Licenses may be revoked by the Arbitration Committee for doping,
    match-fixing, repeated plagiarism or an ethics violation.

3.6 Salary caps apply per level (PRO: 5,000,000; SEMI: 750,000).

---

## Article 4 — Clubs and Leagues

4.1 A club must hold a CCIFA club licence to compete.

4.2 Rosters are between 5 and 25 coders, with at least 3 PRO licenses.

4.3 Leagues award 3 points for a win, 1 for a draw, 0 for a loss.

4.4 Promotion and relegation apply the top-2 / bottom-2 rule.

4.5 Tiebreakers, in order: points, goal difference, goals for, head
    to head, fair play.

4.6 Continental leagues exist for each confederation; the World Cup
    is the quadrennial final tournament.

---

## Article 5 — Drafts and Transfers

5.1 An annual draft is held; the order is the reverse of the previous
    season's ranking (weakest club picks first).

5.2 Eligibility: minimum age 16, amateur or semi license, no prior
    PRO contract.

5.3 Three rounds; each club picks one coder per round.

5.4 Transfers happen only inside official windows and require both
    clubs' signatures, the coder's signature, a medical and the
    federation's sign-off.

5.5 Financial Fair Play caps salary-to-revenue ratio at 0.7.

---

## Article 6 — Official Matches and the Sovereign Seal

6.1 Official matches are played 100% offline in sovereign arenas.

6.2 The arena network must be **physically severed** during the match.

6.3 Each official match has exactly one presiding arbiter, who signs
    the Sovereign Seal with an Ed25519 key.

6.4 The seal comprises a root hash (SHA-256 of the canonical match
    payload), the signature, and a chain hash linking to the previous
    sealed event.

6.5 The sealed record is exported from the arena by a sworn courier
    on physical media (USB) and imported into MatchCore.

6.6 No seal, no result. A match without a valid Sovereign Seal is
    null and void.

---

## Article 7 — Arbitration

7.1 Arbiters are accredited by the Arbitration Committee for a
    renewable two-year term.

7.2 Each official match has one presiding arbiter.

7.3 Arbiters may issue four decisions: VALID, INVALID, PENALTY,
    DISQUALIFY.

7.4 Appeals are allowed within 48 hours; the Arbitration Committee
    reviews them.

7.5 Arbiters are bound by the Arbiters Charter.

---

## Article 8 — World Cup

8.1 The Coding World Cup is the quadrennial final tournament of CCIFA.

8.2 Each confederation organises qualifiers; the host rotates
    among the five confederations.

8.3 The finals format comprises a group stage, a knockout bracket and
    a single final.

8.4 The winner of the final is crowned World Champion of sport-coding.

8.5 Every World Cup match is an official match and is sealed.

---

## Article 9 — Sovereignty of the Ledger

9.1 The Sovereign Ledger is the single source of truth for every
    CCIFA event.

9.2 The ledger is append-only; entries cannot be edited or deleted.

9.3 Verification is deterministic and replayable from the genesis hash.

9.4 Any party may verify the ledger at any time via the MatchCore
    REST endpoint `POST /ledger/verify`.

9.5 A ledger that fails verification is void; the federation must
    declare a continuity incident (see the BCP).

---

## Article 10 — Final Provisions

10.1 These Regulations are certified in 11 languages; the English
     master text prevails in case of inconsistency.

10.2 Amendments require a two-thirds majority of the Executive
     Committee and ratification by the General Assembly.

10.3 These Regulations enter into force on the date of their sealing.

10.4 Any matter not covered is governed by the Sport-Coding
     Committee, subject to appeal to the Arbitration Committee.

---

## CCIFA Certification Block

| Field | Value |
|------|-------|
| Document | CCIFA Official Regulations |
| Language | English (master) |
| Version | v1.0 |
| Issued by | CCIFA Executive Committee |
| Certified languages | EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR |
| Seal | SHA-256(ccifa-legal-regulations) |
| Status | Certified |

> This document is certified in all 11 CCIFA Certified Languages. In the
> event of any inconsistency, the English master text shall prevail.

> **Sovereign Ledger reference**: this charter is anchored to the
> Sovereign Ledger by its root hash and may be verified at any time via
> the MatchCore REST endpoint `GET /seals/{root}`.

Certified by the **CCIFA Executive Committee** on behalf of the Code &
Craft International Federation Association.
