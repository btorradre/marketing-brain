"""Unified cost ledger. Every engine wrapper calls log_cost() after a spend
so 'what did concept X cost' is answerable in one place instead of being
rediscovered per-pipeline (see reference_kie_api / reference_higgsfield_seedance_true_cost
memories: get_cost lies, pre-auth != actual charge, credit types don't mix).

Prefer the ACTUAL credits the provider reports (e.g. kie's creditsConsumed)
over estimate_credits() — the estimator is only for pre-flight budget checks
before firing a request that costs real money.
"""

import db

# credits -> USD, per engine. Verified 2026-08: kie ~= $0.004/credit (reference_kie_api.md).
CREDIT_USD_RATE = {
    "kie": 0.004,
}

# (engine, model) -> credits per second, for PRE-FLIGHT budget checks only.
# Source: reference_kie_api.md / reference_higgsfield_seedance_true_cost.md memories.
KNOWN_RATES_PER_SECOND = {
    ("kie", "bytedance/seedance-2-5"): 63.0,   # flat, 720p+audio, validated 2026-08-07
    ("kie", "bytedance/seedance-2"): 41.0,     # actual charge; pre-auth reserves ~3x this
    ("kie", "kling-3.0/video"): 14.0,          # repriced 2026-08-06
}


def estimate_credits(engine: str, model: str, duration_s: float | None = None) -> float | None:
    if duration_s is None:
        return None
    rate = KNOWN_RATES_PER_SECOND.get((engine, model))
    return round(rate * duration_s, 2) if rate is not None else None


def log_cost(job_id: str | None, engine: str, credits: float | None = None,
             note: str | None = None) -> None:
    usd = round(credits * CREDIT_USD_RATE[engine], 4) if (
        credits is not None and engine in CREDIT_USD_RATE) else None
    db.record_cost(job_id, engine, credits=credits, usd_estimate=usd, note=note)


def summary(brand: str | None = None, concept: str | None = None) -> dict:
    return db.cost_summary(brand=brand, concept=concept)
