# Build notes — MENSID-01 stills

**9/01: kie gpt-image-2 rejects LONG prompts at 2K** ("The current content could not be
processed"), reproduced 2/2 on the full ~11k-char block prompt; the SAME prompt succeeds
at 1K, and short prompts succeed at 2K. Isolation: every individual block passes, full
prompt passes at 1K up to 10.9k chars. So the approval pass renders at **1K** and only
the approved picks get upscaled before animation. Do not silently switch back to 2K.
Probe cost: ~7.5cr per 1K success, 10cr at 2K. Failures consume 0.
