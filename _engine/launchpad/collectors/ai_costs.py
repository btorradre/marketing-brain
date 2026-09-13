"""AI spend this week (Sunday-to-date).

- Claude Code: parses local session logs (~/.claude/projects/**/*.jsonl),
  dedupes by message id + request id, prices at public API rates
  (Fable $10/$50, Opus $5/$25, Sonnet $3/$15, Haiku $1/$5 per MTok;
  cache reads 0.1x input, cache writes 1.25x input). This is an
  *estimated value at API rates* — Brooks is on a subscription, so it's
  a usage gauge, not a bill.
- kie.ai credit balance (1 cr ~ $0.004).
- ElevenLabs character usage for the current billing cycle.
"""
import json, os, glob
from datetime import datetime
from .common import env, http_json, week_start

CLAUDE_PROJECTS = os.path.expanduser("~/.claude/projects")

# $ per million tokens: (input, output); cache read = 0.1x in, cache write = 1.25x in
PRICING = [
    ("fable", (10.0, 50.0)),
    ("mythos", (10.0, 50.0)),
    ("opus", (5.0, 25.0)),
    ("sonnet", (3.0, 15.0)),
    ("haiku", (1.0, 5.0)),
]


def _price(model):
    m = (model or "").lower()
    for key, p in PRICING:
        if key in m:
            return p
    return (5.0, 25.0)


def _claude_code_week():
    wk = week_start()
    wk_ts = wk.timestamp()
    seen = set()
    by_model = {}
    by_day = {}
    total_cost = 0.0

    files = glob.glob(os.path.join(CLAUDE_PROJECTS, "*", "*.jsonl"))
    for f in files:
        try:
            if os.path.getmtime(f) < wk_ts:
                continue
            for line in open(f, errors="replace"):
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                if e.get("type") != "assistant":
                    continue
                msg = e.get("message") or {}
                usage = msg.get("usage")
                ts = e.get("timestamp")
                if not usage or not ts:
                    continue
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
                except Exception:
                    continue
                if dt < wk:
                    continue
                key = (msg.get("id"), e.get("requestId"))
                if key in seen:
                    continue
                seen.add(key)
                model = msg.get("model", "unknown")
                if model == "<synthetic>":
                    continue
                inp = usage.get("input_tokens", 0)
                out = usage.get("output_tokens", 0)
                cw = usage.get("cache_creation_input_tokens", 0)
                cr = usage.get("cache_read_input_tokens", 0)
                pi, po = _price(model)
                cost = (inp * pi + out * po + cw * pi * 1.25 + cr * pi * 0.1) / 1e6
                total_cost += cost

                mm = by_model.setdefault(model, {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "cost": 0.0, "calls": 0})
                mm["input"] += inp; mm["output"] += out
                mm["cache_write"] += cw; mm["cache_read"] += cr
                mm["cost"] += cost; mm["calls"] += 1

                day = dt.strftime("%Y-%m-%d")
                by_day[day] = by_day.get(day, 0.0) + cost
        except Exception:
            continue

    for m in by_model.values():
        m["cost"] = round(m["cost"], 2)
    return {
        "week_start": wk.isoformat(),
        "total_cost": round(total_cost, 2),
        "by_model": {k: v for k, v in sorted(by_model.items(), key=lambda kv: -kv[1]["cost"])},
        "by_day": {k: round(v, 2) for k, v in sorted(by_day.items())},
        "note": "Claude Code usage valued at public API rates (subscription gauge, not a bill)",
    }


def _kie():
    key = env("KIE_API_KEY")
    if not key:
        return {"error": "KIE_API_KEY not set"}
    data, _ = http_json("https://api.kie.ai/api/v1/chat/credit",
                        headers={"Authorization": f"Bearer {key}"})
    credits = data.get("data")
    if isinstance(credits, dict):
        credits = credits.get("credits") or credits.get("credit")
    return {"credits": credits, "usd_value": round(float(credits) * 0.004, 2) if credits is not None else None,
            "auto_topup": True}


def _elevenlabs():
    key = env("ELEVENLABS_API_KEY")
    if not key:
        return {"error": "ELEVENLABS_API_KEY not set"}
    data, _ = http_json("https://api.elevenlabs.io/v1/user/subscription",
                        headers={"xi-api-key": key})
    return {
        "tier": data.get("tier"),
        "characters_used": data.get("character_count"),
        "characters_limit": data.get("character_limit"),
        "next_reset_unix": data.get("next_character_count_reset_unix"),
    }


def collect():
    out = {}
    for name, fn in [("claude_code", _claude_code_week), ("kie", _kie), ("elevenlabs", _elevenlabs)]:
        try:
            out[name] = fn()
        except Exception as e:
            out[name] = {"error": str(e)[:200]}
    return out
