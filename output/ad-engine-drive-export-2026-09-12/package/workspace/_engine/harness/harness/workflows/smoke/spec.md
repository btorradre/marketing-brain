## Job

Prove the harness plumbing works. Three steps, then stop.

1. Call `dr_status`. Then call `dr_load_brand` for the brand in the run block (skip if brand is null).
2. Attempt to call `mcp__ad-engine__kie_generate` once with any input. The harness must deny it because the `generate` flag is off. Note the denial reason you received.
3. Write `report.md` in the run directory with the required sections. Under `## Outcome` state which tools succeeded and quote the denial reason. Under `## Blocked on Brooks` write `nothing`. End with `RUN COMPLETE`.

Do nothing else.
