## Job

Turn one reference video ad into a law-compliant adaptation for our brand and product: watched frame by frame, autopsied as a strategist, redirected (never traced), scripted in prose, gated by the laws, and delivered as a two-lane Cutroom storyboard Brooks can approve. This run does not generate images, video, or voice. It ends when the board is pushed.

## Steps, in order. Do not skip or reorder.

1. **Orient.** Call `dr_pipeline_guide`, then `dr_load_brand` for the brand. Call `dr_get_playbook("laws")`. Load the product-truth skill for the product (the Skill tool; the name follows `<brand>-<product>`) and keep its identity block verbatim for later. Note the brand's angle bank and any prior concepts for this product from `dr_list_artifacts`.

2. **Verify product truth live.** Every spoken claim in the final script must map to a real, current feature. Use WebFetch on the live product page before writing claims. If the product page and the skill disagree, the live page wins and you say so in the report.

3. **Resolve and watch the reference.** `resolve_reference_tool` on the input URL or path, then `watch_reference_tool` on the resolved media. Never adapt a reference you have not watched. Build the scene ledger: one row per staged scene (location, prop, people, beat job, spoken lines), cut rhythm, and the energy curve. Cuts are not scenes; a prop entering or leaving hands is a scene boundary.

4. **Autopsy the reference as a strategist.** In writing, before any script line: angle, claims ladder, emotional engine per act, promise plus identity upgrade, belief channeling, the golden nugget, and one beat job per scene. Save it with `dr_save_artifact` as an adaptation-plan artifact.

5. **Redirect for our product.** This is the mirror-fidelity law and the never-trace law applied together, and they do not conflict. MIRROR the skeleton: beat functions and order, shot types, compositions, cut rhythm, energy curve, pacing, staging logic. The reference lane and our lane line up beat for beat. REINVENT the surface: our creator, our setting, our dialogue, our claims, our product's real mechanics. Never copy dialogue verbatim and never keep a claim our product cannot demonstrate; replace it with the strongest true claim that does the same job in that slot. Apply the swap test to the angle; if a competitor's product fits, rewrite the angle before writing a line. Apply the six-month test. Port the reference's script FLOW (connectives, sentence rhythm, the concession move), not just its topics. If Brooks gave an angle constraint in the inputs, it governs.

6. **Write the script as prose.** Complete spoken sentences a person would say out loud. No staccato fragments. No em dashes. Numerals for numbers. Creator says "they" and "their," never "our" or "we." Every claim gets a demonstration beat on screen. Product visible for the entire ad. Run `dr_lawgate` on the script with the brand and speaker set. Fix every blocker and re-run until clean. Save the script with `dr_save_artifact`.

7. **Log the concept.** `dr_push_concept` with product, concept name, angle, and thesis so the tracker has a row before the board exists.

8. **Create the editing plan automatically.** Follow `_engine/sops/Ad-Editing-Plan-First-SOP.md`. Verify the actual reference cut boundaries and transition spans against consecutive source frames; a watch manifest is not a complete frame audit. Save the reference cut/VO/B-roll/flow analysis and a concrete editing plan in the concept's `edit/` folder before any downstream production. Map every proposed line to its visual/action, source or gap, provisional duration, cut/transition, movement, captions, audio and purpose. Include hook, product reveal, CTA/end hold, chosen editor and delivery checks. Reference existing accepted plans and update them on revisions. This planning step introduces no additional approval gate.

9. **Build the board.** `dr_push_brief_board` with a two-lane spec: lane one is the reference (one card per scene with the reference frame, timecode, and what the beat does), lane two is our version (one card per scene with script line, visual direction, emotion, product-truth notes, and a keyframe prompt-sketch). Use the frames the watcher extracted for the reference lane. The board title carries the naming convention id from the concept.

10. **Report.** Write `report.md` in the run directory using the sections named in the run block. Link the saved editing plan and reference evidence. Under `## Blocked on Brooks`, write exactly what needs approval on the board and the board URL. Then end with `RUN COMPLETE`.

## Hard rules for this workflow

- Mirror the skeleton, never trace the surface. A one-to-one copy of dialogue or claims is a failure even if it would render perfectly; a board whose beats do not line up with the reference lane is also a failure.
- Strategist before director. No script before the autopsy is saved.
- Sell our product, not the category. The swap test is mandatory.
- Birkin, Hermes, and competitor names never appear in scripts, prompts, or board cards.
- No generation of any kind. If a step seems to need a generated image, write the prompt sketch on the card instead.
- If the reference cannot be resolved or watched, stop, write the report with the failure, and end. Do not invent scenes from a thumbnail.
