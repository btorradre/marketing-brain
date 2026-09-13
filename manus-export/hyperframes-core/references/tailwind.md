# Tailwind projects

Some projects are scaffolded to use a browser-runtime build of Tailwind CSS (pinned version `@tailwindcss/browser@4.2.4` — treat it as Tailwind v4, not an older v3 setup). Signs a project uses this: `index.html` contains `window.__tailwindReady`; the task asks for Tailwind utility classes, `@theme`, custom utilities, or v3-to-v4 fixes; rendered frames show missing styles or a frame-0 flash of unstyled content.

Do not replace the scaffolded runtime with an unpinned Tailwind CDN script — that defeats reproducibility. Keep the readiness shim deterministic; the renderer waits for `window.__tailwindReady` before capturing frame 0. For offline / locked-down / production-stable renders, compile Tailwind to a CSS file and ship the stylesheet instead of the browser runtime.

## v4 browser runtime rules

Tailwind v4 is CSS-first:

```html
<style type="text/tailwindcss">
  @theme {
    --color-brand: oklch(0.68 0.2 252);
    --font-display: "Inter", sans-serif;
  }

  @utility headline-balance {
    text-wrap: balance;
    letter-spacing: 0;
  }
</style>
```

Avoid v3-only patterns:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Do not add a JS config file only for composition colors, fonts, spacing, or utilities — use `@theme` and `@utility` instead. Migrating from v3? Load an existing JS config explicitly with `@config "./tailwind.config.js";` inside a `text/tailwindcss` block — v4 does not auto-detect v3 config files.

## Composition pattern

Use Tailwind for static layout and style; keep render-critical timing in GSAP or another seekable runtime.

```html
<section
  id="hero"
  class="clip absolute inset-0 grid place-items-center bg-zinc-950 text-white"
  data-start="0"
  data-duration="5"
  data-track-index="1"
>
  <div class="w-[1280px] max-w-[82vw] text-center">
    <h1 class="text-7xl font-black leading-none text-balance">Render-ready Tailwind</h1>
  </div>
</section>
```

For repeated items, parameterize via CSS variables — keep the class list static so the runtime sees every utility:

```html
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 0"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 1"></span>
<span class="translate-y-[calc(var(--i)*6px)] opacity-80" style="--i: 2"></span>
```

## Dynamic class safety

The browser runtime scans classes it can see — do not build render-critical class names only at seek time:

```js
// Risky: the runtime may never see every generated class.
element.className = `bg-${color}-500`;
```

Prefer complete class tokens in HTML, data-attribute variants, or explicit CSS:

```html
<div data-tone="blue" class="bg-blue-500 data-[tone=rose]:bg-rose-500"></div>
```

If a generated class is truly unavoidable, make sure the full class token still appears somewhere as a static string in a `text/tailwindcss` block before validation.

## Video-specific guardrails (every bullet is a hard rule)

- **Stable dimensions only** — use `w-[…]` / `h-[…]` / `aspect-video` / grid / flex. No `md:`/`lg:` breakpoints — the renderer is a fixed viewport.
- **Animate via transforms/opacity** — `translate-*`, `scale-*`, `opacity-*` are seek-safe; animating Tailwind sizing utilities is not.
- **No `transition-*` for render-critical motion** — a seekable runtime (GSAP) must own the state.
- **No interaction variants** — `hover:`/`focus:`/`active:`/`group-*:`/`peer-*:`/scroll/pointer variants never fire during a render.
- **Bare `border` is broken in v4** — v4's default is `currentColor` (v3 was `gray-200`). Always write the color explicitly: `border border-white/20`.
- **v4 utility renames** — `shadow-sm` → `shadow-xs`, `rounded-sm` → `rounded-xs`, `outline-none` → `outline-hidden`, `flex-shrink-*` → `shrink-*`, `flex-grow-*` → `grow-*`.
- **Modern CSS is fine** — `color-mix()`, container queries, logical properties all work; the renderer runs current Chrome.

## Quick debug checklist

When Tailwind styles don't apply in a render, check in order: is the project actually scaffolded for Tailwind? Does `index.html`'s `<head>` load the pinned browser-runtime script (not an unpinned CDN)? Is the `window.__tailwindReady` promise present? Are there any leftover v3 `@tailwind` directives? Have config tokens moved into `@theme` (or an explicit `@config` reference for v3 migration)? Does every render-critical class appear as a complete static token (no string-built class names)? Then re-run validation and do a quick draft render to prove frame 0 isn't flashing unstyled content — preview alone can hide that defect.
