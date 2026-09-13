# Worked Examples

## Adding a block

**Scenario:** an existing HyperFrames project needs an animated chart added alongside existing video content.

### 1. Install the block

```bash
hyperframes add data-chart
```

### 2. Wire into index.html

```html
<div id="stage" data-composition-id="main" data-width="1920" data-height="1080" data-duration="30">
  <video
    id="speaker"
    src="speaker.mp4"
    data-start="0"
    data-duration="30"
    data-track-index="0"
    style="position: absolute; width: 60%; height: 100%; left: 0; top: 0; object-fit: cover;"
  ></video>

  <!-- Data chart appears at 5s in the right 40% of the screen -->
  <div
    data-composition-id="data-chart"
    data-composition-src="compositions/data-chart.html"
    data-start="5"
    data-duration="15"
    data-track-index="1"
    data-width="1920"
    data-height="1080"
    style="position: absolute; right: 0; top: 0; width: 40%; height: 100%;"
  ></div>
</div>
```

### 3. Lint and preview

```bash
hyperframes lint
hyperframes preview
```

### 4. Customize (optional)

Edit `compositions/data-chart.html` — data arrays are at the top of the script, colors are in the CSS rules scoped under `[data-composition-id="data-chart"]`.

---

## Adding a component

**Scenario:** add a shimmer light-sweep effect to a title text element.

### 1. Install the component

```bash
hyperframes add shimmer-sweep
```

### 2. Read the snippet

Open `compositions/components/shimmer-sweep.html` and read the comment header.

### 3. Wire into your composition

**HTML** — wrap target elements:

```html
<div class="shimmer-sweep-target" style="--shimmer-color: rgba(255, 255, 255, 0.5)">
  <h1 class="title">AI-Powered Video</h1>
</div>
```

**CSS** — paste the `.shimmer-sweep-target` and `.shimmer-mask` rules from the snippet.

**JS** — paste the auto-injection script (before timeline code):

```js
document.querySelectorAll(".shimmer-sweep-target").forEach((el) => {
  if (!el.querySelector(".shimmer-mask")) {
    const mask = document.createElement("div");
    mask.className = "shimmer-mask";
    el.appendChild(mask);
  }
});
```

**Timeline** — add the sweep:

```js
tl.fromTo(
  ".shimmer-sweep-target",
  {
    "--shimmer-pos": "-20%",
  },
  {
    "--shimmer-pos": "120%",
    duration: 1.2,
    ease: "power2.inOut",
    stagger: 0.15,
  },
  1.5,
);
```

### 4. Lint and preview

```bash
hyperframes lint
hyperframes preview
```

### 5. Customize

- `--shimmer-color`: highlight color per element
- `--shimmer-width`: light band width (default 20%)
- `--shimmer-angle`: sweep direction (default 120deg)
- Timeline `duration`, `ease`, `stagger`: control speed and feel
