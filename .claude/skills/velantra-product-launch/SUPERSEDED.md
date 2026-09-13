# Superseded by `product-launch` (2026-08-22)

Use `.claude/skills/product-launch/` instead. This folder is kept only for the
`launch_state.json` record of the Bow Tote launch (2026-07-02).

Why it was replaced:

- `generate_angles.py` fired **nano-banana**, which violates the standing law that all
  product i2i goes through GPT Image 2.
- `gen_editorial.py` shelled out to the **Higgsfield CLI**, which is dead on this machine
  (`Error: Not authenticated`, interactive browser login).
- Every script used `urllib`, which has no CA bundle here and needed an `SSL_CERT_FILE`
  export to run at all. The replacement is curl-backed throughout.
- Images were attached with **no `#color_` alt tags**, so galleries leaked across colorways.
- The PDP builder imported a `build_templates.py` with per-product content hardcoded in a
  dict, including origin claims that are banned ("Tuscan tannery", "New York atelier",
  "LWG Gold"). The replacement clones a live donor template and sweeps inherited claims.
- Theme id and store were resolved in ways that assumed a theme that has since been
  republished.

No product-truth or launch history is lost: nothing here is referenced by another skill.
