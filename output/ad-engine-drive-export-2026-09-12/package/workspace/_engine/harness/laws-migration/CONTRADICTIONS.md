# Contradictions found during the 2026-09-03 law migration

Surfaced by the migration pass over all 117 `feedback_*.md` memory files. Each needs a ruling from Brooks. Until ruled, both laws sit in `house-laws.md` and the run has to reason about scope.

1. **Brand-name timing.** `tof_no_product_first_seconds` (brand lands about a third in) and `ugc_demonstrate_never_describe` (name the brand late, ~36s) vs `velantra_ad_script_formula` ("This is the [Name] from Velantra" by 0:06) and `sell_our_product_not_the_category` (reveal about 0:07). Likely scope: TOF UGC vs the greenscreen VO formula. Not stated anywhere.
2. **Hook shape.** `ugc_demonstrate_never_describe` (open mid-thought, flat, no superlative) vs `velantra_ad_script_formula` (verdict or reversal inside the hook).
3. **Ken Burns.** `no_kenburns_fill_use_real_footage` (never) vs `broll_engine_rule_omni_vs_seedance`, `omni_macro_mutation`, `omni_11_flash_and_gemini_37_flash` (hero-product beats and failed macros go Ken Burns from the approved keyframe).
4. **Real vs generated humans in action slots.** `real_footage_for_action_broll` (any generated human fails the cut) vs `one_creator_element_lock`, `broll_must_advance_story`, `ugc_one_continuous_scene`, `weekender_no_real_iphone_stills_in_ads` (generated continuous creator b-roll; AI assets only). Probably Motilli VSL vs Velantra. Never stated.
5. **Animated-ad engine.** `animated_replicator` (Veo 3.1, never Kling) vs `animated_video_hardwon_rules` (Kling 5s segments) and the `animated-video` skill (Kling 3.0 native audio).
6. **"Velantra" TTS respelling.** `elevenlabs_v3_creative_vo` (`Vell-Ahn-Trah`; `Vehlantra` failed) vs `tts_respell_hyphens_cause_pauses` (hyphens cause pauses; plain `Vehlantra` works).
7. **HeyGen voice vs the v3 IVC law.** `heygen_avatar_v_woman_over_40_default` (always the Woman Over 40 library voice) vs `elevenlabs_v3_needs_ivc_not_pvc` (library PVCs read flat on v3, clone a creator). Whether Woman Over 40 is a PVC is not recorded.
8. **Seedance prompt format.** `ugc_dialogue_naturalness` (short-prompt law is dead, dense UGC Director format) vs `segment_brief_standard` (dense JSON retired, simple 4-part blocks), two days apart. Engine split (Seedance vs Omni) is implied.
9. **Birkin.** `velantra_no_competitor_comparisons` (Hermes and Birkin stay out) vs `velantra_birkin_inspired_mechanism` (reversed 8/21) vs `birkin_angle_stays_on_birkin_references` (9/1). `brands/velantra/ops/claude-project-instructions.md` reportedly still says Birkin stays out.
10. **Italian leather.** `velantra_origin_claims` carve-out approves "softest Italian leather", but `examples/velantra.json` `no-origin-claims` still flags `italian leather` as a warning.
11. **Deliver assets vs finished cut.** `deliver_assets_not_edits` vs the second correction in `omni_over_seedance_cost` ("create and edit the video" means a finished cut for VO and product ads).
12. **Pinterest creator refs.** `seedance_ugc_pinterest_creators` still states Pinterest-per-run as current; MEMORY.md marks it RETIRED 9/1 with no updated file.
13. **Motilli canonical product reference path.** Four different paths across `product_shots_i2i`, `motilli_gummy_color`, `animated_replicator`.
14. **Clip duration.** `fixed_6s_video_segments` (every i2v clip 6s) vs `animated_video_hardwon_rules` (Kling max 5s) vs `segment_brief_standard` (Omni 8 to 10s). Per engine, never reconciled.

## Classification calls to confirm

- Casting law (`creator_casting_white_women_only`, LAW 8/31): encoded as both a prompt-scope regex blocker and a Generation judgment law. The regex is blunt; judgment-only may be preferable.
- Product-scoped bans (Vivienne "structured/rigid"; Meridian "never blue" interior; Meridian "rolled handles + front flap") are judgment-only under Brand-specific: Velantra because the JSON schema has no product field and "structured" is a required word for Sofia, Delphine, and Meridian.
- `no-affordable-luxury-phrase` is a warning: 7/23 says internal-only, 7/28 says the phrase is fine.
- `signal-is-nerve-not-bacteria` is a warning: false-positive risk against the current top-not-bottom mechanism.
- Brief-format laws sit under Delivery and QA; MEMORY.md says the creative-brief lane is unsettled.

15. **Mirror vs never-trace.** `reference_mirror_fidelity` and the ad-engine MCP instructions ("reference adaptations MIRROR the reference: same beats, shots, compositions, pacing, our product swapped in") vs the `seedance-directors-cut` skill ("Never trace. Creator, setting, dialogue and claims are always re-invented"). Surfaced by the first harness run (VEL-WEEKENDER-ONEBAG-01, 2026-09-03). The reference-adapt workflow spec now reconciles them as "mirror the skeleton, reinvent the surface." Confirm that reading.
