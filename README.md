 <!-- ██████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗     ██████╗██╗   ██╗██████╗ 
██╔════╝██╔═══██╗██╔══██╗██║████╗  ██║██╔════╝     ██║    ██║██╔═══██╗██╔══██╗██║    ██╔═══██╗   ██╔════╝██║   ██║██╔══██╗
██║     ██║   ██║██║  ██║██║██╔██╗ ██║██║  ███╗    ██║ █╗ ██║██║   ██║██████╔╝██║    ██║   ██║   ██║     ██║   ██║██████╔╝
██║     ██║   ██║██║  ██║██║██║╚██╗██║██║   ██║    ██║███╗██║██║   ██║██╔══██╗██║    ██║   ██║   ██║     ██║   ██║██╔═══╝ 
╚██████╗╚██████╔╝██████╔╝██║██║ ╚████║╚██████╔╝    ╚███╔███╔╝╚██████╔╝██║  ██║███████╗╚██████╔╝   ╚██████╗╚██████╔╝██║     
 ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝     ╚═════╝ ╚═════╝ ╚═╝     
                                                                                                                      
███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗ ██████╗ ██████╗ ██████╗ ███████╗
████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
██╔████╔██║███████║   ██║   ██║     ███████║██║     ██║   ██║██████╔╝█████╗  
██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║██║     ██║   ██║██╔══██╗██╔══╝  
██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║╚██████╗╚██████╔╝██║  ██║███████╗
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                                                                                          
 ██████╗ ██████╗ ██╗███████╗ █████╗ 
██╔════╝██╔════╝ ██║██╔════╝██╔══██╗
██║     ██║      ██║█████╗  ███████║
██║     ██║      ██║██╔══╝  ██╔══██║
╚██████╗╚██████╗ ██║██║     ██║  ██║
 ╚═════╝ ╚═════╝ ╚═╝╚═╝     ╚═╝  ╚═╝ -->

                          Code & Craft International Federation Association
                            The sovereign engine of the Coding World Cup


> MatchCore lives **ONLINE** and governs every dimension of sport-coding life:
> federations, confederations, leagues, clubs, drafts, licenses, transfers,
> rankings, calendars, arbitration, matches and the World Cup itself.
> Only the **official matches** are played **100% offline**, in sovereign arenas,
> and every match is sealed by a chained SHA-256 hash + Ed25519 arbiter signature.

---

## Table of contents

1. [Vision](#vision)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Project layout](#project-layout)
5. [Quick start](#quick-start)
6. [The Sovereign Seal](#the-sovereign-seal)
7. [Certified languages](#certified-languages)
8. [Roadmap](#roadmap)
9. [Governance](#governance)
10. [License](#license)

---

## Vision

CCIFA — the **Code & Craft International Federation Association** — is the
international federation governing the **Coding World Cup**, a global
sport-coding competition built on the four craft domains of *Coder*,
*Designer*, *Maker* and *Strategist*.

MatchCore is the **living, online, sovereign engine** that manages every
sport-coding life cycle: federation structure, five continental
confederations, national and continental leagues, clubs and rosters,
annual drafts, licenses, transfers, rankings, calendars, arbitration,
matches, and the quadrennial World Cup.

MatchCore is *online* and *living*: federations breathe, calendars move,
rankings update in real time. But when the bell rings for an **official
match**, the world goes dark: the arena is **offline**, the network is
**physically severed**, and the only thing that comes back out is a sealed,
chained, signed record. The match result is **sovereign**.

---

## Architecture

```
                        ┌────────────────────────────────────────────┐
                        │              DASHBOARD (React/TS)            │
                        │  i18n • 11 langs • TanStack Query • Zustand  │
                        └───────────────────┬────────────────────────┘
                                            │ HTTPS / WSS
                            ┌───────────────▼───────────────┐
                            │      GATEWAY (Caddy / Nginx)    │
                            └───────────────┬───────────────┘
                                            │
   ┌────────────────────────────────────────▼────────────────────────────────┐
   │                            MATCHCORE  (FastAPI)                           │
   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
   │  │Federation│ │  League  │ │   Club   │ │  Coder   │ │  Arbitration │  │
   │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
   │  │  Draft   │ │ Transfer │ │ Calendar │ │  Match   │ │   Ranking    │  │
   │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
   │  ┌──────────────────────────────────────────────────────────────────┐  │
   │  │                       RULE ENGINE  (YAML v1.0)                    │  │
   │  └──────────────────────────────────────────────────────────────────┘  │
   │  ┌──────────────────────────────────────────────────────────────────┐  │
   │  │   SEAL ENGINE   ── chained SHA-256 ── Ed25519 arbiter signature   │  │
   │  └──────────────────────────────────────────────────────────────────┘  │
   │  ┌──────────────────────────────────────────────────────────────────┐  │
   │  │              SOVEREIGN LEDGER  (append-only JSONL)                │  │
   │  └──────────────────────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────┬───────────────────────────────┘
                                             │ physical USB / signed courier
                              ┌──────────────▼──────────────┐
                              │    ARENA NODES (offline)     │
                              │  no network  •  sealed HSM   │
                              └─────────────────────────────┘
```

---

## Features

### Federation & Confederations
- 5 continental confederations: **AF** (Africa), **AM** (Americas),
  **AS** (Asia), **EU** (Europe), **OC** (Oceania).
- Full CCIFA organigram: President, Executive Committee, Sport-Coding
  Committee, Arbitration Committee, Ethics & Integrity Committee.

### Leagues & Clubs
- National leagues, continental leagues and the World Cup.
- Round-robin and bracket calendars, automatic promotion / relegation.
- Clubs with rosters, budgets, sponsors and transfer windows.

### Coders & Licenses
- Three license levels: **PRO**, **SEMI**, **AMATEUR**.
- Four craft domains: **Coder**, **Designer**, **Maker**, **Strategist**.
- National-team eligibility rules and cap tracking.

### Draft & Transfers
- Annual draft with weighted order, eligibility windows and pick signing.
- Transfer windows with validation, medical and arbiter sign-off.

### Official Matches & the Sovereign Seal
- Friendly matches run online; **official** matches run **100% offline**.
- Every official match is sealed:
  - **root hash** — SHA-256 of the canonical match payload,
  - **signature** — Ed25519 from the presiding arbiter,
  - **chain hash** — SHA-256 of `prev_chain_hash || root_hash`.
- Seals are append-only and immutable in the Sovereign Ledger.

### Arbitration & Sovereign Ledger
- Arbiters issue decisions: **VALID**, **INVALID**, **PENALTY**,
  **DISQUALIFY**.
- Sovereign Ledger is a SHA-256 chained JSONL log; verification is
  deterministic and replayable from genesis.

### World Cup
- Biennial final tournament with group stage, knockout, final.
- National teams selected from each confederation's qualifiers.

### Internationalisation
- 11 certified languages: **EN, FR, ES, IT, DE, HI, PT, JA, ZH, KO, AR**.
- Dashboard, legal corpus and docs all localised.

---

## Project layout

```
ccifa-coding-world-cup/
├── README.md                      # this file
├── LICENSE                        # CCIFA Sovereign License v1.0
├── .env.example
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── matchcore/
│   ├── engine/                    # the sovereign engine (Python)
│   │   ├── core/                   # domain models
│   │   ├── arena/                  # offline arena nodes
│   │   ├── ledger/                 # sovereign ledger
│   │   ├── api/                    # FastAPI REST
│   │   └── cli/                    # matchcore CLI
│   ├── rules/v1.0/                 # YAML rule pack
│   ├── infra/                      # docker, k8s, monitoring, chaos
│   └── tests/                      # unit, offline sim, load (k6)
├── dashboard/                      # React + TS dashboard
│   ├── src/
│   └── public/locales/             # 11 certified languages
├── legal/                          # certified legal corpus
│   ├── en/                         # master
│   └── fr/                         # certified copy
├── docs-site/                      # Astro Starlight docs
├── status-site/                    # Astro Starlight status
├── worldcup-site/                  # Astro Starlight World Cup showcase
├── scripts/                        # operational scripts
└── .github/workflows/              # CI / load / chaos
```

---

## Quick start

### Prerequisites
- Python 3.12+
- Node 20+ and `pnpm` (or `npm`)
- Docker 24+ and Docker Compose v2
- `make` (optional but recommended)

### 1. Clone & install

```bash
git clone https://github.com/ccifa/coding-world-cup.git
cd coding-world-cup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Boot the full stack

```bash
make docker-up            # postgres, redis, matchcore, dashboard, meilisearch, minio
make migrate
make seed
```

### 3. Run the engine locally (without Docker)

```bash
make run                   # uvicorn matchcore.engine.api.rest:app --reload
```

### 4. Simulate a season

```bash
python scripts/simulate_season.py
```

### 5. Run the dashboard

```bash
cd dashboard
pnpm install
pnpm dev                   # http://localhost:5173
```

---

## The Sovereign Seal

A Sovereign Seal is the cryptographic guarantee that an official match
was played in a sovereign arena, arbitrated, and recorded immutably.

```json
{
  "root_hash":   "sha256(canonical_match_payload)",
  "signature":   "ed25519(root_hash, arbiter_private_key)",
  "arbiter":     "ARBITER-0007",
  "chain_hash":  "sha256(prev_chain_hash || root_hash)",
  "prev_chain_hash": "...",
  "ledger_index": 4271,
  "sealed_at":   "2026-11-06T20:00:00Z"
}
```

Verification is a one-liner:

```python
from matchcore.engine.core.seal_engine import SealEngine
assert SealEngine(public_key=arbiter_pk).verify(seal, match_payload)
```

---

## Certified languages

| Code | Language     | Native name        |
|------|--------------|--------------------|
| en   | English      | English            |
| fr   | French       | Français           |
| es   | Spanish      | Español            |
| it   | Italian      | Italiano           |
| de   | German       | Deutsch            |
| hi   | Hindi        | हिन्दी               |
| pt   | Portuguese   | Português          |
| ja   | Japanese     | 日本語               |
| zh   | Chinese      | 中文                |
| ko   | Korean       | 한국어               |
| ar   | Arabic       | العربية             |

---

## Roadmap

- [x] v0.1 — federation, confederations, leagues, clubs, coders
- [x] v0.2 — drafts, transfers, calendars
- [x] v0.3 — match engine + seal engine + sovereign ledger
- [x] v0.4 — FastAPI REST + CLI
- [x] v0.5 — React/TS dashboard with 11-language i18n
- [x] v0.6 — Astro docs, status and World Cup sites
- [x] v0.7 — infra (Docker, K8s, monitoring) + CI/CD
- [ ] v1.0 — first certified World Cup cycle

---

## Governance

CCIFA is governed by the **Executive Committee**, the **Sport-Coding
Committee**, the **Arbitration Committee** and the **Ethics & Integrity
Committee**. See `legal/en/CCIFA-OFFICIAL-REGULATIONS.md` for the full
statutes.

---

## License

Released under the **CCIFA Sovereign License v1.0** — see [LICENSE](LICENSE).
