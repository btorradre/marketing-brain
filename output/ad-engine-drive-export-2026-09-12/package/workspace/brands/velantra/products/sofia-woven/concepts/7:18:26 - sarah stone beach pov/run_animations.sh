#!/bin/bash
# Runs all 8 Straw Tote POV animations sequentially (resumable — completed ones skip).
# Needs ~1040 kie credits available per task start; actual charge ~328 each (~2,624 total).
cd "$(dirname "$0")"
RUNNER="/Users/brooksorradre2/Documents/marketing brain/.claude/skills/pov-trend-factory/scripts/pov_factory.py"
for d in VEL-POV-BEACHBAG-01 VEL-POV-BEACHBAG-02-caban-black VEL-POV-BEACHBAG-03-cream \
         VEL-POV-BEACHBAG-04-lady-pink VEL-POV-BEACHBAG-05-light-chocolate \
         VEL-POV-BEACHBAG-06-lightning-orange VEL-POV-BEACHBAG-07-sky-blue \
         VEL-POV-BEACHBAG-08-sunny-yellow; do
  echo "=== $d"
  python3 "$RUNNER" animate "$d/job.json" || echo "FAILED: $d"
done
echo "All animations attempted. QA + trim + finish comes next."
