# Velantra product scale and visual fidelity

This protocol supports the 16 product skills built from the September 4, 2026 catalog audit. It applies to product photographs, generated stills, model scenes and video frames. A convincing image is not evidence of a physical measurement.

## Select the exact product and evidence

Resolve the product family, Shopify handle, color, size and construction revision through `registry.json`. Duplicate Shopify listings may share a product skill, but their IDs, variant bindings and media histories remain separate. Match the selected reference to the intended shipped SKU. A competitor's dimensions or a similar-looking bag are not Velantra measurements.

These constraints govern faithful depictions of existing products. A later explicit redesign request can change a proposed concept; label it as a concept and keep it separate from records of the existing product and manufactured samples.

Separate evidence along two axes:

- **Manufactured product evidence:** dated sample measurements, supplier drawings tied to a SKU/revision, actual product photographs and real footage.
- **Creative/design evidence:** an owner-approved master or requested hardware/color modification. This can establish the intended visual design without proving the manufactured product has that design or size.

An old generated picture is never an independent source of dimensions or hidden construction. A field called `approved`, `real`, `master` or `product truth` is not sufficient provenance. Read its lineage. If real goods, owner direction and catalog content disagree, record the disagreement and use the matching evidence for the task; do not silently certify a shipped product from a design target.

## Dimension status

| Status | Meaning | Permitted conclusion |
| --- | --- | --- |
| physically_measured | A dated physical sample, identified SKU/revision, defined endpoints and measurement method are recorded. | That sample measured this value under the recorded conditions. |
| supplier_documented | A supplier dimension photograph or drawing identifies this model. | Supplier-stated dimensions; not proof every shipped unit was measured. |
| owner_approved | Brooks approved a nominal design/specification. | Approved target dimensions, not a factory measurement. |
| catalog_only | A storefront, theme, fulfillment transcription or marketing document contains the value. | Published/recorded dimensions with measurement provenance unverified. |
| inferred | A value came from visual estimates, a similar bag or proportional inference. | Estimate only; never publish as measured. |
| unknown | No supported value was recovered. | No numerical size claim. |
| conflicting | Sources disagree or dimension axes/model identity are unresolved. | Preserve candidates and resolve the conflict before size-specific production. |

Status belongs to each measurement, not only to the product. Width may be supplied while handle drop remains unknown. Copying a PDP figure into a fulfillment sheet is one source lineage, not independent corroboration.

## Define what is being measured

Record front width at the **top opening** and **base** separately when they differ; body height from base to rim excluding handles; maximum external depth with gussets in a stated position; handle drop from rim to underside of the handle apex; and detachable strap length between specified attachment points. Record empty/filled, open/closed, upright/slumped and expanded/cinched states. Record internal opening/usable dimensions separately for fit claims.

Accessories need their own endpoints: charm body versus total hanging length, ring outer diameter, scarf unfolded length/width, organizer outer dimensions by size. Do not measure packaging instead of the product. Do not transfer a handbag's dimensions to its keychain.

Use exact unit arithmetic: 1 inch = 2.54 cm. Retain the precision of the source; a decimal conversion does not improve an approximate measurement. Normalize tables to **front W × body H × D** while preserving the original axis order. An unlabeled 19 × 18 × 14 cm tuple must stay unlabeled until the axes are established.

## Prepare the image

Use **GPT Image 2** with the exact product/color/angle reference. Keep dimensions in the prompt as constraints, together with the observed silhouette, gusset depth, handle/body ratio and closure geometry. A number in a prompt alone cannot lock scale.

For white studio images, use a neutral white seamless background, broad diffused light and a soft contact shadow. Preserve the product's actual color and material response: matte wool/suede/felt, canvas weave, leather grain and local sheen, and the exact metal finish. Keep fill gentle enough to retain weave, nap, edge thickness and cavity shadows. Lighting is an art-direction choice; it cannot change product construction.

Prefer the existing verified camera view for a background/lighting edit. New back, side, bottom, interior, open-closure or packing views need corresponding construction evidence. Do not invent hidden pockets, lining, feet, long straps or closure components. Do not erase a conflicting detail simply because another product in the line has a cleaner design.

For videos, use **Google Omni** and the approved product references. Inspect beginning, middle and end for scale and construction drift. Use the internal video editor only when actual editing is required. HyperFrames remains banned.

## Check two different kinds of accuracy

**Reference-relative fidelity:** compare source and output at the same orientation and bag state. Mark body landmarks, width/height silhouette, rim/base endpoints, handle attachments, handle drop, panel seams, gussets and hardware positions. Normalize by a shared body width when comparing differently framed images. For a background-only edit, product landmarks should remain fixed apart from a uniform scale/translation of the whole product. Do not stretch width and height separately to force a match. Image canvas size and percent frame occupancy are not real-world size.

**Metric scale:** requires a supported physical/supplier dimension plus an independently established scale anchor in the same plane and depth, or a camera-calibrated scene. A model's presumed height, unknown handbag, generic phone, laptop diagonal, ring or hand is not an exact ruler. Foreshortened three-quarter width cannot be directly compared with a frontal measurement. A single image also cannot verify an unseen depth.

For a planar calibrated view, estimated dimension = product span in pixels ÷ anchor span in pixels × measured anchor length. Record the endpoints, anchor source, perspective assumptions, uncertainty and tolerance before judging. Use separate front and side views to assess W/H/D. A scale check reports agreement with the recorded reference under those assumptions; it does not certify manufacturing tolerances. If the anchor or dimensions are missing, mark metric scale **not verifiable**, while continuing work that can preserve evidenced proportions.

A controlled comparison showing several products must share a recorded pixels-per-cm scale and camera geometry. Individually centered ecommerce cards need not show every bag at identical frame occupancy; do not describe such a grid as a literal size comparison.

## Accept or hold by issue

Record the selected source image, source lineage, output, variant, view/state, dimension values/status, known scale anchor, identity review, material/color review and unresolved issues. Inspect detailed crops for hardware, seams and print, plus the whole product silhouette.

Reject an output that changes observable construction, color binding, print, hardware count/location or required proportions. Hold size-specific lifestyle, capacity, comparison or dimension claims when measurements/anchors are absent or conflicting. A reference-matched isolated packshot may be retained with **physical scale unverified**; do not label it fully dimension-accurate.

Real measured product photographs preserve absolute-size evidence better than repeated regeneration. When exact printed motifs or complex open mechanisms drift repeatedly, retain the original product pixels through an appropriate production workflow instead of treating more prompt text as verification.

## Measurement handoff

For each outstanding SKU obtain a front/ruler photo, side/ruler photo and detail of relevant handle/strap measurement; identify color, model revision and measurement date. For soft bags include empty and lightly filled states. Confirm material composition from a supplier specification rather than texture alone. `measurement-gaps.md` lists the product-specific unresolved fields. This task does not authorize contacting suppliers or publishing changes.
