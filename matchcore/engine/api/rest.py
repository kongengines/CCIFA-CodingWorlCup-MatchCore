"""MatchCore FastAPI REST API.

Exposes every domain object as JSON. Endpoints:

- GET  /health
- GET  /federation
- GET  /confederations
- GET  /leagues
- GET  /clubs
- GET  /coders
- GET  /matches
- POST /matches/{id}/play
- GET  /drafts
- GET  /rankings
- GET  /worldcup
- GET  /seals/{root}
- POST /ledger/verify
"""

from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from matchcore.engine.core.coder import Coder, CraftDomain
from matchcore.engine.core.club import Club
from matchcore.engine.core.match import Match, MatchKind
from matchcore.engine.core.matchcore import MatchCore
from matchcore.engine.core.license import LicenseLevel


# -- single shared engine instance ----------------------------------------- #
def _build_engine() -> MatchCore:
    mc = MatchCore(
        rules_path=os.environ.get("MATCHCORE_RULES_PATH", "matchcore/rules/v1.0"),
        ledger_path=os.environ.get("SEAL_LEDGER_PATH", "matchcore/data/sovereign-ledger.jsonl"),
        arbiter_private_key=os.environ.get("ARBITER_PRIVATE_KEY"),
        arbiter_public_key=os.environ.get("ARBITER_PUBLIC_KEY"),
    )
    mc.accredit_arbiter("ARBITER-0001")
    mc.accredit_arbiter("ARBITER-0002")
    return mc


app = FastAPI(
    title="MatchCore — CCIFA Coding World Cup",
    description="The living, online, sovereign engine of sport-coding.",
    version="0.7.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("MATCHCORE_CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine: MatchCore = _build_engine()


# -- request models -------------------------------------------------------- #
class PlayRequest(BaseModel):
    home_score: int
    away_score: int
    arbiter_id: str | None = None


class VerifyRequest(BaseModel):
    pass


# -- routes ---------------------------------------------------------------- #
@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "engine": repr(engine),
        "rules_version": engine.rules.version,
        "ledger_entries": len(engine.ledger),
        "ledger_verified": engine.ledger.verify(),
    }


@app.get("/federation")
def federation() -> Dict[str, Any]:
    return engine.federation.to_dict()


@app.get("/confederations")
def confederations() -> Dict[str, Any]:
    return {"confederations": [c.to_dict() for c in engine.federation.all_confederations()]}


@app.get("/leagues")
def leagues() -> Dict[str, Any]:
    return {"leagues": [l.to_dict() for l in engine.leagues.values()] or []}


@app.get("/clubs")
def clubs() -> Dict[str, Any]:
    return {"clubs": [c.to_dict() for c in engine.clubs.values()]}


@app.get("/coders")
def coders() -> Dict[str, Any]:
    return {"coders": [c.to_dict() for c in engine.coders.values()]}


@app.get("/matches")
def matches() -> Dict[str, Any]:
    return {"matches": [m.to_dict() for m in engine.matches.values()]}


@app.post("/matches/{match_id}/play")
def play_match(match_id: str, req: PlayRequest) -> Dict[str, Any]:
    if match_id not in engine.matches:
        raise HTTPException(404, f"Match {match_id} not found")
    m = engine.play_match(match_id, req.home_score, req.away_score,
                          arbiter_id=req.arbiter_id)
    return m.to_dict()


@app.get("/drafts")
def drafts() -> Dict[str, Any]:
    return {"drafts": [d.to_dict() for d in engine.drafts.values()]}


@app.get("/rankings")
def rankings() -> Dict[str, Any]:
    return {"ranking": engine.ranking.to_dict()}


@app.get("/worldcup")
def worldcup() -> Dict[str, Any]:
    # The World Cup is the quadrennial final tournament.
    return {
        "name": "Coding World Cup",
        "cycle": "quadrennial",
        "next_edition": 2026,
        "confederations": [c.to_dict() for c in engine.federation.all_confederations()],
        "rankings": engine.ranking.to_dict()[:8],
    }


@app.get("/seals/{root_hash}")
def get_seal(root_hash: str) -> Dict[str, Any]:
    for e in engine.ledger:
        seal = e.get("event", {}).get("seal") or {}
        if isinstance(seal, dict) and seal.get("root_hash") == root_hash:
            return seal
    raise HTTPException(404, f"Seal with root_hash={root_hash} not found")


@app.post("/ledger/verify")
def verify_ledger(_: VerifyRequest | None = None) -> Dict[str, Any]:
    return engine.ledger.to_dict()
