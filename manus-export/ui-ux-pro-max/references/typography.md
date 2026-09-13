# Typography & Color (Priority 6 — MEDIUM)

## Core rules

- Line-height 1.5-1.75 for body text.
- Line length 65-75 characters.
- Pair heading and body fonts whose personalities match (not fighting each other).
- Use a consistent type scale (e.g. 12/14/16/18/24/32).
- Use noticeably darker text on light backgrounds (e.g. a near-black on white, not mid-gray).
- Use a platform type-role system (iOS Dynamic Type styles / Material type roles — display, headline, title, body, label) rather than ad hoc sizes.
- Use font-weight to reinforce hierarchy: bold headings (600-700), regular body (400), medium labels (500).
- Define semantic color tokens (primary, secondary, error, surface, on-surface) rather than scattering raw hex values through component code.
- In dark mode use desaturated/lighter tonal variants, not simply inverted colors — and test contrast in dark mode separately from light mode.
- Foreground/background pairs must meet at least 4.5:1 contrast (AA) or 7:1 (AAA) — verify with a contrast-checking tool.
- Functional colors (error red, success green) must be paired with an icon or text, never rely on color alone to convey meaning.
- Prefer text wrapping over truncation; when truncation is unavoidable, use an ellipsis and provide the full text via a tooltip or expand affordance.
- Respect the platform's default letter-spacing; avoid tight tracking on body text.
- Use tabular/monospaced figures for data columns, prices, and timers, to prevent digits from causing layout shift as they change.
- Use whitespace intentionally to group related items and separate sections — avoid visual clutter.

## Light/dark mode contrast (app)

| Rule | Do | Don't |
|---|---|---|
| Surface readability (light) | Cards/surfaces clearly separated from background via opacity/elevation | Overly transparent surfaces that blur hierarchy |
| Text contrast (light) | Body text contrast ≥4.5:1 against light surfaces | Low-contrast gray body text |
| Text contrast (dark) | Primary text ≥4.5:1, secondary text ≥3:1, on dark surfaces | Dark-mode text that blends into the background |
| Border/divider visibility | Separators visible in both themes | Theme-specific borders that disappear in one mode |
| State contrast parity | Pressed/focused/disabled states equally distinguishable in both themes | Interaction states defined for only one theme |
| Token-driven theming | Semantic color tokens mapped per theme across surfaces/text/icons | Hardcoded per-screen hex values |
| Scrim and modal legibility | Modal scrim strong enough to isolate foreground content (~40-60% black) | Weak scrim that leaves the background visually competing |

## Related reference files

- 73 curated heading/body font pairings (each with Google Fonts URL, CSS `@import`, and Tailwind config) live in `references/typography-pairings.md`.
- 161 product-type color palettes (primary/secondary/accent/background/foreground/card/muted/border/destructive/ring, each as a hex token) live in `references/color-palettes.md`.
- The source vault also has a raw `google-fonts.csv` catalog of ~1,900 individual Google Fonts (family, category, stroke, classification, popularity/trending rank) for advanced one-off font lookups beyond the 73 curated pairings — not reproduced here due to size; use the 73 curated pairings first.

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` Typography category (6 rows) and `app-interface.csv` Typography + Theming categories (3 rows).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 72 | Typography | Line Height | All | Adequate line height improves readability | `Use 1.5-1.75 for body text` | `Cramped or excessive line height` | `leading-relaxed (1.625)` | `leading-none (1)` | Medium |
| 73 | Typography | Line Length | Web | Long lines are hard to read | `Limit to 65-75 characters per line` | `Full-width text on large screens` | `max-w-prose` | `Full viewport width text` | Medium |
| 74 | Typography | Font Size Scale | All | Consistent type hierarchy aids scanning | `Use consistent modular scale` | `Random font sizes` | `Type scale (12 14 16 18 24 32)` | `Arbitrary sizes` | Medium |
| 75 | Typography | Font Loading | Web | Fonts should load without layout shift | `Reserve space with fallback font` | `Layout shift when fonts load` | `font-display: swap + similar fallback` | `No fallback font` | Medium |
| 76 | Typography | Contrast Readability | All | Body text needs good contrast | `Use darker text on light backgrounds` | `Gray text on gray background` | `text-gray-900 on white` | `text-gray-400 on gray-100` | High |
| 77 | Typography | Heading Clarity | All | Headings should stand out from body | `Clear size/weight difference` | `Headings similar to body text` | `Bold + larger size` | `Same size as body` | Medium |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 26 | Typography | Base Font Size | fontScale dynamic type | iOS/Android/React Native | Body text must be readable and support Dynamic Type | `Use platform fontScale and at least 14–16pt base` | `Render critical text below 12pt` | `<Text style={{ fontSize: 16 }}>Body</Text>` | `<Text style={{ fontSize: 10 }}>Body</Text>` | High |
| 27 | Typography | Dynamic Type Support | allowFontScaling adjustsFontSizeToFit | iOS/Android/React Native | Support system text scaling without breaking layout | `Set allowFontScaling and test large text` | `Disable scaling on all text globally` | `<Text allowFontScaling>{label}</Text>` | `<Text allowFontScaling={false}>{label}</Text>` | High |
| 29 | Theming | Light/Dark Contrast | dark mode contrast tokens | iOS/Android/React Native | Ensure sufficient contrast in both light and dark themes | `Use semantic tokens and test both themes` | `Reuse light-theme grays directly in dark mode` | `colors.textPrimaryDark = '#F9FAFB'` | `colors.textPrimaryDark = '#9CA3AF' on '#111827'` | High |
