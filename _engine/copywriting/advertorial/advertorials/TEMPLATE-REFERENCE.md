# Motilli GLP-1 Advertorial Template Reference

Use this file as the blueprint when building new advertorial variations. Keep the same HTML structure, design components, images, and CTA links — only swap out the copy.

---

## Template Source File
`/glp1-v2/index.html`

---

## Tech Stack
- Plain HTML (no build tools, no React)
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Google Fonts: **Merriweather** (serif, body text) + **Inter** (sans-serif, headings/UI)
- Tailwind config extends fontFamily with `sans: ['Inter']` and `serif: ['Merriweather']`
- Custom `.highlight` class: yellow background (`#fef08a`) with 4px padding

---

## Images (Keep These Exact URLs)

| Position | URL | Alt Text |
|----------|-----|----------|
| Hero (after header) | `https://i.ibb.co/7tcRV7PL/Gemini-Generated-Image-73ogva73ogva73og.jpg` | Doctor explaining GLP-1 side effects to patient |
| Below "Upstream Blockage" heading | `https://i.ibb.co/rfwFhCCk/m2.jpg` | Diagram showing stomach paralysis and fermentation from GLP-1 medications |
| Below "Why Food Rots" heading | `https://i.ibb.co/fYTDs3P3/stomach.jpg` | Stomach diagram showing food fermentation |
| Below "vicious cycle" quote | `https://i.ibb.co/YFcs9Cw8/mechanism-explanation.jpg` | Mechanism explanation diagram |
| Below "Three gummies" quote | `https://i.ibb.co/8DrnV7Jn/m4.jpg` | Motilli product image |
| Below "What Patients Report" heading | `https://i.ibb.co/rGH4vHyX/r1.jpg` | Patient results and reports |

Image HTML pattern:
```html
<div class="w-full rounded-xl overflow-hidden shadow-sm my-8">
    <img alt="ALT TEXT" class="w-full h-auto block" src="IMAGE_URL">
</div>
```

---

## CTA Links
All CTA buttons point to: `https://trymotilli.co/products/motilli-celery-juice-gummies`
All open in new tab: `target="_blank" rel="noopener noreferrer"`

---

## Page Structure & Design Components

### 1. Sticky Header
- Brand name: "Gut Health Insider" (blue-900, uppercase, font-black)
- "Advertorial" label (gray-400, uppercase, tiny)
- Blue accent line (bg-blue-900 h-1)
- Sticky top, z-50

### 2. Sticky Bottom CTA Bar
- Fixed bottom, z-100, green (#8cc63f) background
- "Check Availability" text, uppercase, extrabold
- Full-width block link

### 3. Article Header
- H1: font-sans, extrabold, 3xl/5xl
- H2: font-serif, italic, xl/2xl, gray-600
- Byline bar: brand name | date | read time with clock SVG icon

### 4. Article Body
- `font-serif text-lg md:text-[20px] text-gray-900 leading-[1.8] space-y-8`
- Paragraphs: plain `<p>` tags
- Bold text: `<strong class="font-bold">`
- Section headings: `<h3 class="font-sans font-bold text-2xl text-gray-900 mt-12 mb-4">`

### 5. Blockquotes (Doctor Quotes)
```html
<p class="font-sans text-lg italic text-gray-600 border-l-4 border-gray-300 pl-4 py-2 my-8">"Quote text"</p>
```

### 6. Scenario Boxes (Red-tinted, for problems)
```html
<div class="bg-red-50 border border-red-200 rounded-xl p-6">
    <p><strong class="font-sans font-bold text-gray-900">Scenario A: Title</strong></p>
    <p class="text-base text-gray-700 mt-2">Description</p>
</div>
```

### 7. Numbered Problem/Pathway Boxes (Gray, with blue circle numbers)
```html
<div class="bg-gray-50 border border-gray-200 rounded-xl p-6">
    <div class="flex items-start gap-4">
        <div class="flex-shrink-0 w-8 h-8 bg-blue-900 text-white rounded-full flex items-center justify-center font-sans font-bold text-sm">1</div>
        <div>
            <h4 class="font-sans font-bold text-lg text-gray-900 mb-1">Title</h4>
            <p class="text-base text-gray-700">Description</p>
        </div>
    </div>
</div>
```

### 8. Timeline Cards (Green-tinted, for patient results)
```html
<div class="bg-green-50 border border-green-200 rounded-xl p-6">
    <div class="flex items-start gap-4">
        <div class="flex-shrink-0 w-10 h-10 bg-green-600 text-white rounded-full flex items-center justify-center font-sans font-bold text-xs">1-3d</div>
        <div>
            <h4 class="font-sans font-bold text-lg text-gray-900 mb-1">Days 1-3</h4>
            <p class="text-base text-gray-700">Description</p>
        </div>
    </div>
</div>
```

### 9. Final CTA Card
- bg-gray-50 border rounded-xl, centered text
- Red button (#D32F2F) with hover, shadow, transform effects
- Disclaimer text below button

### 10. Footer
- Gray background, copyright, privacy/terms/contact links
- Medical disclaimer in tiny text

---

## Section Order (for new variations, swap copy but keep this structure)

1. **Sticky Header** (Gut Health Insider + Advertorial)
2. **Sticky Bottom CTA Bar** (green, fixed)
3. **Article Header** (H1 headline, H2 subheadline, byline)
4. **Hero Image**
5. **Opening paragraphs** (hook/pain point)
6. **Section: "Upstream Blockage"** + image + doctor quotes
7. **Section: "Why Food Rots"** + image + doctor quotes
8. **Section: "The Laxative Trap"** + Scenario A/B boxes + quotes
9. **Section: "The Three Problems"** + numbered boxes + quote + mechanism image
10. **Section: "Why Just Juice Celery Doesn't Work"** + quotes
11. **Section: "A New Approach"** + Motilli intro + product image + pectin/vitamins quotes
12. **Section: "What Patients Report"** + image + timeline cards + quote
13. **Section: "The Question to Ask Yourself"** + closing paragraphs
14. **Final CTA Card** (red button + disclaimer)
15. **Footer**

---

## Deployment
- Deploy with: `cd glp1-vX && npx vercel --yes --prod`
- Project auto-links to Vercel org: bto-ec-ventures

---

## Current Live Versions
- glp1-v2: https://glp1-v2.vercel.app
