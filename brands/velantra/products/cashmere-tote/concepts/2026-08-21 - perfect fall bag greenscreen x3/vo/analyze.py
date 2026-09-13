#!/usr/bin/env python3
"""Measure dead space and pause-variance (robotic-ness proxy) from EL word timings."""
import json, sys, statistics as st, os

for p in sys.argv[1:]:
    W = json.load(open(p))
    gaps = [round(W[i+1]["s"] - W[i]["e"], 3) for i in range(len(W)-1)]
    total = W[-1]["e"]
    lead = W[0]["s"]
    dead = sum(g for g in gaps if g > 0.15) + lead
    speech = total - dead
    big = [g for g in gaps if g > 0.15]
    name = os.path.basename(p).replace("-words.json","")
    # coefficient of variation on inter-word gaps: low CV = metronomic = robotic
    cv = (st.pstdev(gaps)/st.mean(gaps)) if gaps and st.mean(gaps) > 0 else 0
    print(f"{name:<26} total {total:5.2f}s  deadair {dead:5.2f}s ({dead/total*100:4.1f}%)  "
          f"speech {speech:5.2f}s  pauses>{0.15}s: {len(big):2d}  maxgap {max(gaps):.2f}s  gapCV {cv:.2f}")
