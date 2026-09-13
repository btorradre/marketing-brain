#!/usr/bin/env python3
"""
Categorize — assign every raw transaction a P&L category + bucket, then rebuild the ledger.

Layers, in order (first decisive answer wins):
  0. locked rows (manual decisions, legacy Meta-API rows, supplier bills) are never touched
  1. source exclusion hints (Plaid "Excluded - credit card payment/internal transfer") → cc_payment / transfer
  2. vendor rulebook  config/vendor_rules.json  (regex on merchant, then description)      confidence 0.90
  3. provided category from a legacy interop export                                          confidence 0.70
  4. Plaid business_category / personal_finance_category hints                               confidence 0.50
  5. --llm: Claude classifies what is still unknown or low-confidence                        model confidence
Anything below --threshold (default 0.8), flagged `review` by its rule, or still unknown goes to
data/review_queue.json for Brooks/Claude to rule on (review.py). Unknown rows are exported to the
ledger as other_opex (cat_source=unreviewed) so profit is never overstated while they wait.

The ledger (shopify-financials/data/expenses.json) is REBUILT from transactions.json on every run;
the previous ledger is backed up next to it first.

Usage:
  python3 categorize.py                 # rules + hints, rebuild ledger, refresh review queue
  python3 categorize.py --llm           # also ask Claude about the leftovers (needs ANTHROPIC_API_KEY in .env)
  python3 categorize.py --llm --provider openai            # same, but GPT 5.6 Sol classifies (OPENAI_API_KEY in .env)
  python3 categorize.py --second-opinion [--limit 200]     # GPT 5.6 Sol re-reads categorized rows; cross-bucket disagreements → queue
  python3 categorize.py --recategorize  # re-run rules on every unlocked row (after editing the rulebook)
  python3 categorize.py --summary       # month × bucket totals, no changes
"""
import os, re, sys, json, argparse, shutil, datetime as dt
from collections import defaultdict, Counter
from fin_common import *  # noqa

PLAID_MAP = {  # business_category (from the Plaid-style export) -> (category, confidence)
    "advertising": ("ad_spend_other", 0.55), "software / saas": ("software_saas", 0.5), "meals": ("meals_entertainment", 0.6),
    "travel": ("travel", 0.6), "office / misc shopping": ("office_misc", 0.5), "office / rent": ("office_misc", 0.6),
    "banking / taxes": ("merchant_fees", 0.4), "inventory": ("inventory_purchase", 0.6), "miscellaneous": ("other_opex", 0.3),
    "uncategorized / needs review": ("other_opex", 0.2), "needs review - transfer-like outflow": ("other_opex", 0.2),
    "excluded - credit card payment": ("cc_payment", 0.9),
}
PFC_MAP = {  # personal_finance_category_detailed prefixes
    "food_and_drink": ("meals_entertainment", 0.55), "travel": ("travel", 0.55), "transportation": ("travel", 0.5),
    "general_services_advertising": ("ad_spend_other", 0.5), "bank_fees": ("merchant_fees", 0.6),
    "loan_payments_credit_card": ("cc_payment", 0.9), "transfer_out": ("transfer", 0.5), "transfer_in": ("transfer", 0.5),
    "government_and_non_profit_tax": ("taxes_gov", 0.7), "rent_and_utilities": ("office_misc", 0.6),
    "general_merchandise": ("office_misc", 0.4), "entertainment": ("meals_entertainment", 0.4),
}
BRAND_WORDS = [(re.compile(rf"\b{b}\b", re.I), b) for b in BRANDS]


def load_rules():
    d = load_json(RULES, {"rules": []})
    out = []
    for r in d["rules"]:
        try:
            out.append((re.compile(r["pattern"], re.I), r))
        except re.error as e:
            print(f"  bad rule pattern '{r.get('name')}': {e}")
    return out


def infer_brand(t):
    for rx, b in BRAND_WORDS:
        if rx.search(t["description"]): return b
    return None


def apply_rules(t, rules):
    for rx, r in rules:
        if rx.search(t["merchant"]) or rx.search(t["description"]):
            return r
    return None


def classify_local(t, rules):
    """Returns (category, source, confidence, needs_review, reason)."""
    h = t.get("hints", {})
    if h.get("excluded_by_source"):
        cat = "cc_payment" if re.search(r"payment|apple card|amex|american express", t["description"], re.I) else "transfer"
        return cat, "hint:excluded", 0.95, False, "source marked excluded (card payment / transfer)"
    r = apply_rules(t, rules)
    if r:
        return r["category"], f"rule:{r['name']}", 0.9, bool(r.get("review")), r.get("note") or f"matched rule '{r['name']}'"
    pc = h.get("provided_category")
    if pc in CATEGORIES:
        return pc, "hint:provided", 0.7, False, "category supplied by the export"
    bc = str(h.get("business_category", "")).strip().lower()
    if bc in PLAID_MAP:
        cat, conf = PLAID_MAP[bc]
        return cat, "hint:plaid_business", conf, conf < 0.6, f"Plaid business_category '{bc}'"
    det = str(h.get("personal_finance_category_detailed", "")).strip().lower()
    for pref, (cat, conf) in PFC_MAP.items():
        if det.startswith(pref):
            return cat, "hint:plaid_pfc", conf, conf < 0.6, f"Plaid detail '{det}'"
    return None, None, 0.0, True, "no rule or hint matched"


# ------------------------------------------------------------------ LLM layer
def _load_env_key():
    envp = os.path.join(BRAIN, ".env")
    if not os.path.exists(envp): return
    for line in open(envp):
        for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
            if line.startswith(k + "=") and not os.environ.get(k):
                os.environ[k] = line.split("=", 1)[1].strip().strip('"').strip("'")


LLM_SYSTEM = """You are the bookkeeper for a portfolio of DTC ecommerce brands (Velantra — leather/canvas bags; Motilli — gut-health gummies; Lunessa, Solorna, Renavita — supplements). The owner is Brooks; he travels a lot and mixes business + personal spend on business cards.

Classify each bank/card transaction into EXACTLY one category key from this list:
{taxonomy}

Buckets the P&L rolls up to: marketing (paid ads, marketing tools, creators), ai (LLM subscriptions/API usage, image/video/voice generation, AI writing/detection, AI coding tools), operating (everything else that runs the company), cogs (3PL, freight), excluded (transfers, card payments, owner draws, loan principal).

House rulings:
- Any AI product = ai_tools even if it is used for marketing (Higgsfield, ElevenLabs, HeyGen, Manus, OpenRouter, Anthropic, OpenAI, GPTZero, WriteHuman, Adnova, Blort, Magnific, Pixelcut, kie.ai, Runway, Kling...).
- Ad-intel/spy tools, email/SMS platforms, creative-editing software (CapCut, Frame.io, Adobe, Canva) = marketing_software.
- Shopify subscription/app charges = software_saas (Shopify payment-processing fees come from the API, never the bank).
- Venmo / Wise / Zelle to individuals = contractors_agency unless clearly personal. Upwork = contractors_agency.
- Disputifier = chargeback_services. Intuit/QuickBooks = legal_professional.
- Card bill payments (American Express Payment, Apple Card payment, ACH to card) = cc_payment. Shopify payouts and moves between the owner's own accounts = transfer.
- Supplier wires to the manufacturer (Haikou Genyangkai) = inventory_purchase.
- Personal-looking spend (apparel, gym, spa, streaming, casinos, university) → other_opex with confidence ≤ 0.5 and a note; do NOT invent a business purpose.
- brand: set only when the description clearly names a brand or a brand-specific vendor; else null.

Return ONLY a JSON array, one object per input id, no prose:
[{"id": "...", "category": "<key>", "brand": "<Brand or null>", "confidence": 0.0-1.0, "reason": "<≤12 words>"}]"""


def _payload(chunk, with_current=False):
    out = []
    for t in chunk:
        o = {"id": t["id"], "date": t["date"], "account": t["account"], "amount": t["amount"],
             "description": t["description"], "hints": {k: v for k, v in t.get("hints", {}).items()
                                                        if k in ("business_category", "personal_finance_category_detailed", "memo", "hint")}}
        if with_current and t.get("category"):
            o["current_category"] = t["category"]; o["current_source"] = t.get("cat_source")
        out.append(o)
    return out


def _parse_results(text, label):
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        print(f"  {label}: no JSON array in reply"); return {}
    try:
        arr = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        print(f"  {label}: bad JSON ({e})"); return {}
    res = {}
    for o in arr:
        cat = norm_category(o.get("category"))
        if o.get("id") and cat:
            res[o["id"]] = {"category": cat, "brand": (o.get("brand") if o.get("brand") in BRANDS else None),
                            "confidence": float(o.get("confidence") or 0.5), "reason": str(o.get("reason") or "")[:120]}
    print(f"  {label}: {len(res)} classified")
    return res


def openai_classify(txns, model="gpt-5.6-sol", batch=40, with_current=False):
    """GPT (5.6 Sol by default) as classifier / second opinion. Same taxonomy + house rulings as Claude."""
    _load_env_key()
    from openai import OpenAI
    client = OpenAI()
    taxonomy = "\n".join(f"- {k}: {v['label']}  [bucket={v['bucket']}]" for k, v in CATEGORIES.items())
    system = LLM_SYSTEM.replace("{taxonomy}", taxonomy)
    if with_current:
        system += ("\n\nSECOND-OPINION MODE: each row carries current_category (assigned by a rulebook or another model). "
                   "Return the category YOU believe is right. Agree when the current one is defensible; disagree only when "
                   "it is clearly wrong under the rulings above, and say why in `reason`.")
    results = {}
    for i in range(0, len(txns), batch):
        chunk = txns[i:i + batch]
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": "Classify these transactions:\n" + json.dumps(_payload(chunk, with_current), ensure_ascii=False)}],
        )
        text = resp.choices[0].message.content or ""
        u = resp.usage
        results.update(_parse_results(text, f"GPT batch {i // batch + 1} (in={u.prompt_tokens} out={u.completion_tokens})"))
    return results


def llm_classify(txns, model="claude-opus-5", batch=40):
    _load_env_key()
    import anthropic
    client = anthropic.Anthropic()
    taxonomy = "\n".join(f"- {k}: {v['label']}  [bucket={v['bucket']}]" for k, v in CATEGORIES.items())
    system = LLM_SYSTEM.replace("{taxonomy}", taxonomy)
    results = {}
    for i in range(0, len(txns), batch):
        chunk = txns[i:i + batch]
        payload = _payload(chunk)
        msg = client.messages.create(
            model=model, max_tokens=16000,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": "Classify these transactions:\n" + json.dumps(payload, ensure_ascii=False)}],
        )
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            print(f"  LLM batch {i // batch + 1}: no JSON array in reply"); continue
        try:
            arr = json.loads(m.group(0))
        except json.JSONDecodeError as e:
            print(f"  LLM batch {i // batch + 1}: bad JSON ({e})"); continue
        for o in arr:
            cat = norm_category(o.get("category"))
            if o.get("id") and cat:
                results[o["id"]] = {"category": cat, "brand": (o.get("brand") if o.get("brand") in BRANDS else None),
                                    "confidence": float(o.get("confidence") or 0.5), "reason": str(o.get("reason") or "")[:120]}
        print(f"  LLM batch {i // batch + 1}: {len(arr)} classified  (in={msg.usage.input_tokens} out={msg.usage.output_tokens}"
              f"{', cache_read=' + str(msg.usage.cache_read_input_tokens) if getattr(msg.usage, 'cache_read_input_tokens', None) else ''})")
    return results


# ------------------------------------------------------------------ ledger export
def export_ledger(T):
    entries = []
    for t in T:
        if t["source"].startswith("supplier_bill"):
            continue  # cross-check data, not a bank outflow — build_pl reconciles it separately
        cat = t["category"] or "other_opex"
        entries.append({"id": t["id"], "month": t["month"], "date": t["date"], "description": t["description"],
                        "amount": t["amount"], "category": cat, "section": CATEGORIES[cat]["section"],
                        "bucket": CATEGORIES[cat]["bucket"], "brand": t.get("brand"), "source": t["source"],
                        "cat_source": t.get("cat_source") or "unreviewed", "confidence": t.get("confidence")})
    entries.sort(key=lambda e: (e["month"], e["category"], e["description"]))
    if os.path.exists(LEDGER):
        bak = LEDGER + f".bak-{dt.date.today().isoformat()}"
        if not os.path.exists(bak): shutil.copy(LEDGER, bak)
    save_json(LEDGER, {"entries": entries, "updated_at": now_iso(), "built_by": "finance-agent/categorize.py"})
    return entries


def summary(T):
    by = defaultdict(float); months = sorted({t["month"] for t in T})
    for t in T:
        b = CATEGORIES[t["category"]]["bucket"] if t["category"] else "UNCATEGORIZED"
        if t["source"].startswith("supplier_bill"): continue
        by[(t["month"], b)] += t["amount"]
    cols = ["marketing", "ai", "operating", "cogs", "excluded", "UNCATEGORIZED"]
    print(f"{'month':8}" + "".join(f"{c:>14}" for c in cols))
    for m in months:
        print(f"{m:8}" + "".join(f"{by.get((m, c), 0):14,.0f}" for c in cols))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--llm", action="store_true", help="classify leftovers with Claude")
    ap.add_argument("--model", default="claude-opus-5", help="Claude model for --llm")
    ap.add_argument("--provider", default="anthropic", choices=["anthropic", "openai"], help="which model does --llm")
    ap.add_argument("--openai-model", default="gpt-5.6-sol")
    ap.add_argument("--second-opinion", action="store_true",
                    help="GPT 5.6 Sol re-reads every unlocked categorized row; disagreements go to the review queue")
    ap.add_argument("--limit", type=int, help="cap rows sent to a model (testing / cost control)")
    ap.add_argument("--threshold", type=float, default=0.8, help="min confidence to skip review")
    ap.add_argument("--recategorize", action="store_true", help="re-run rules on every unlocked row")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--no-export", action="store_true", help="don't rebuild the ledger")
    args = ap.parse_args()

    store = load_json(TXNS, {"transactions": []})
    T = store["transactions"]
    if args.summary:
        summary(T); return
    rules = load_rules()
    stats = Counter(); queue = []
    for t in T:
        if t.get("locked"):
            stats["locked"] += 1; continue
        src0 = t.get("cat_source") or ""
        if t.get("category") and src0 in ("llm", "manual"):
            stats["kept"] += 1; continue          # model/manual answers persist; only rules/hints are re-derived
        if t.get("category") and not args.recategorize and src0.startswith("rule:") and not t.get("needs_review"):
            stats["kept"] += 1; continue
        cat, src, conf, review, reason = classify_local(t, rules)
        t["category"], t["cat_source"], t["confidence"], t["needs_review"], t["reason"] = cat, src, conf, review or conf < args.threshold, reason
        rr = apply_rules(t, rules) if src and src.startswith("rule:") else None
        t["policy"] = rr.get("policy") if rr else None
        if cat and not t.get("brand"):
            r = apply_rules(t, rules)
            t["brand"] = (r.get("brand") if r else None) or infer_brand(t)
        stats[src.split(":")[0] if src else "none"] += 1

    if args.llm:
        todo = [t for t in T if not t.get("locked") and (t["category"] is None or (t.get("confidence") or 0) < args.threshold)]
        if args.limit: todo = todo[:args.limit]
        mname = args.openai_model if args.provider == "openai" else args.model
        print(f"LLM: {len(todo)} transactions to classify with {mname}")
        if todo:
            res = openai_classify(todo, model=args.openai_model) if args.provider == "openai" else llm_classify(todo, model=args.model)
            for t in todo:
                r = res.get(t["id"])
                if not r: continue
                if t["category"] is None or r["confidence"] >= (t.get("confidence") or 0):
                    t["category"], t["cat_source"], t["confidence"] = r["category"], "llm", r["confidence"]
                    t["reason"] = r["reason"]; t["needs_review"] = r["confidence"] < args.threshold
                    if r["brand"]: t["brand"] = r["brand"]
                    stats["llm"] += 1

    if args.second_opinion:
        todo = [t for t in T if not t.get("locked") and t.get("category")]
        if args.limit: todo = todo[:args.limit]
        print(f"Second opinion: {len(todo)} rows → {args.openai_model}")
        res = openai_classify(todo, model=args.openai_model, with_current=True) if todo else {}
        agree = disagree = 0
        for t in todo:
            r = res.get(t["id"])
            if not r: continue
            t["second_opinion"] = {"model": args.openai_model, "category": r["category"], "confidence": r["confidence"], "reason": r["reason"]}
            if r["category"] == t["category"]:
                agree += 1
                if t.get("cat_source") == "llm" and not t.get("needs_review"):
                    t["confidence"] = max(t.get("confidence") or 0, 0.85)  # two models agree
            else:
                disagree += 1
                if r["confidence"] >= 0.7 and CATEGORIES[r["category"]]["bucket"] != CATEGORIES[t["category"]]["bucket"]:
                    t["needs_review"] = True
                    t["reason"] = f"GPT says {r['category']} ({r['confidence']:.2f}): {r['reason']}"
        stats["gpt_agree"], stats["gpt_disagree"] = agree, disagree

    for t in T:
        if t.get("locked"): continue
        if t["category"] is None or t.get("needs_review"):
            queue.append({"id": t["id"], "date": t["date"], "amount": t["amount"], "account": t["account"],
                          "description": t["description"], "merchant": t["merchant"], "proposed": t["category"],
                          "confidence": t.get("confidence"), "reason": t.get("reason"), "brand": t.get("brand"),
                          "policy": t.get("policy"), "second_opinion": t.get("second_opinion")})
    save_json(QUEUE, {"generated_at": now_iso(), "threshold": args.threshold, "items": queue})
    store["updated_at"] = now_iso(); save_json(TXNS, store)

    print("Categorization:", dict(stats))
    print(f"Review queue: {len(queue)} items → {QUEUE}   (python3 review.py --show)")
    if not args.no_export:
        entries = export_ledger(T)
        unrev = sum(1 for e in entries if e["cat_source"] == "unreviewed")
        print(f"Ledger rebuilt: {len(entries)} entries → {LEDGER}   ({unrev} unreviewed rows booked as other_opex)")
    print(); summary(T)


if __name__ == "__main__":
    main()
