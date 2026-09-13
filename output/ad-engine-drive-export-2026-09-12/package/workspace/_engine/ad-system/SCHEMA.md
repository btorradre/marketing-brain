# Shared creative record

Use `ad_system.py new` or `store.blank_record()` to obtain a complete editable record. Use `show` for existing work; preserve its revision on save. The schema is an operating contract, not a claim that populated fields are true.

## Identity and strategy

- `id`: stable letters/digits/hyphen/underscore identifier; `brand`: lowercase slug; `title`; `product`: exact selected product/variant when known.
- `kind`: concept, iteration or variant. Iteration/variant requires `parent_id` and exact `parent_revision`, same brand. Performance-driven children also carry `decision_id`.
- `stage`: intake, research, concept, script, plan, calibration, production, storyboard, editing, review, ready, live, learning, archived. Use `stage` command/UI for checks; do not bypass it in record JSON.
- `strategy`: text fields buyer_situation, awareness, belief_to_change, promise, proof, format, treatment, hypothesis, difference, fixed, changed.
- `format`: heygen-vsl, podcast, skeleton, animated, voiceover-vsl, ugc, product-lifestyle, static. Routing uses this field; `treatment` explains the visual interpretation. Concept comparisons use buying situation, belief, promise and proof, with semantic-review caveats.
- `context_notes`: source context, instructions and explicit uncertainties. `production` uses image_model GPT Image 2, video_model Google Omni, editor DaVinci Resolve.

## Evidence and claims

Each list entry requires a distinct `id` within its collection.

- `evidence[]`: kind observation / quote / product-fact / hypothesis / counterevidence; text; source_path and/or source_url; date; verified boolean. URL-only quotes also require source_excerpt; the quotation must appear verbatim. A local source_path takes precedence and must be a readable text artifact.
- `claims[]`: exact text; evidence_ids list; status supported/unverified/rejected; review_notes explaining why this source substantiates the exact wording and visual implication. `supported` is a reviewer statement, not automatic scientific certification. A hypothesis cannot serve as verified support.
- `approvals[]`: optional historical approval provenance. Does not bypass finished-media or readiness checks; records the user's actual scope/reason rather than inventing a new approval step.

## Story and coverage

- `script`: exact selected narration or static copy. `narration_lock`: null or hash of exact script plus reason/at. Use the UI lock action. A locked narration change requires a supplied user-authorized unlock reason; save clears the old lock.
- `hooks[]`: id, line, visual, test. Spoken line plus visible opening distinguishes hooks; duplicate pairs fail.
- `editing_plan`: accessible saved plan path. `reference_audit`: actual frame-audit path/observations, required if a reference-role artifact is attached. Preserve observed/inferred distinction.
- `beats[]`: id, line, action, story_function, medium, placement, why_line, viewer_response, style_fit, why_here, positive duration in seconds, cut_cue, transition_in, transition_out, source_route, asset_id. Timing stays provisional until final narration alignment; note that in the saved editing plan.
- `medium` describes appearance; `source_route` separately states sourcing/generation/provider gap. Presenter coverage may be deliberate; selection checks exempt `placement: presenter` from covering-asset requirements. Fully animated concepts flag nonanimated media for intentional-hybrid review.

## Assets, artifacts and calibration

- `assets[]`: id, actual path, origin (`sourced|generated|brand-provided`), original source_url when sourced, source_identity/provider ID, inspection with exact interval/action, rights (`unknown|pending|cleared|not-cleared`). Optional sha256 can identify source reuse. Source reuse is a variety flag, not proof of visually distinct compositions; inspect the whole ad.
- TikTok specialization `specialization: tiktok-extreme`: action_match=verified, entry_ev=5, peak_ev=5, rawness>=4, text_status=verified-clean and frame_audit for every selected frame. EV measures visible intensity, not a person's clinical state. Wrong action/text fails even with strong emotion. Other media retain concept-matched criteria.
- `artifacts[]`: id, path, role, status, optional label. Roles include brief, script, editing-plan, reference, status, cutroom-board and export-candidate. Discovered files remain unverified until inspected and selected.
- `cutroom_url`: actual verified storyboard delivery URL. The system does not publish a board by saving this string; the external receipt and real media review must establish delivery.
- `calibration`: reviewed and accepted nonnegative integers, notes, next_action. Accepted cannot exceed reviewed. Zero acceptance flags mismatch review before another bulk run without lowering sourcing criteria.
- `operational`: nullable edit_minutes and recorded rework_count. These are measurements entered from actual work, not inferred from file timestamps.

## Generated system records

- Revisions: immutable record snapshot per save; current record advances by one. Expected-revision mismatch fails. Events append what happened and why.
- Tasks: exact creative revision, kind, state, dependencies, packet, readiness snapshot, owner, lease_until, actual handle, receipt and reconciliation evidence. Lease expiration only signals reconciliation needed. Saved receipt includes actual file hash.
- Reviews: kind automated/human, creative revision, verdict/observations, content hash. Human reviews include reviewer, artifact_path, actual artifact hash and notes. Content excludes stage, timestamps, revision number and operational bookkeeping for staleness; actual content edits invalidate prior reviews. Editing ready/live content returns the current record to review while retaining historical export bindings.
- Exports: creative ID + exact revision + original path + SHA256 + selected hook ID + notes. Registration is idempotent for identical metadata. Hashes establish bytes, not semantic suitability.
- Bindings: platform + account_id + ad_id → exact export. Rebinding an existing ad ID to a different export is rejected to preserve attribution history.
- Imports: source CSV path/content fingerprint, exact reporting settings, errors, original unmatched audit and accepted row IDs. Unmatched state is recomputed when reading measurements.
- Measurements: raw source row, inclusive start/end date window, ad ID, reporting settings, totals and dynamic exact-export join. All overlapping windows for the same ad/settings are rejected, including in a single file.
- Decisions: creative version, selected measurement IDs and source export/version bindings, observation, interpretation, alternative, next_test, fixed, changed and outcome. Distinct matched row IDs required for a performance conclusion. Exact settings must be compatible when aggregating.

## HTTP interface

GET `/api/bootstrap`, `/api/record?id=…[&revision=N]`, `/api/inventory?brand=…`, `/api/results`, `/api/compare?id=A&id=B`, `/api/file?path=…`, `/api/health`.

POST `/api/action` takes JSON with `action` and the fields used by that action. Send `X-Creative-Token` from bootstrap and a same-origin request. Actions: create, save, stage, lock, qa, human-review, queue, task, export, bind, import, decision, iterate, sync. See the small explicit dispatch in `server.py` for exact argument names. No POST action directly invokes an external production service.
