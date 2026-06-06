# Presentations — slide decks, keynotes, hackathon talks

Yuval's slide system is the original source of the Fly High palette. These rules govern decks, keynote captures, conference talks, hackathon presentations, demo screen-recordings, and any slide-based output.

---

## Canvas

- **1920×1080** at 16:9. Always.
- **Padding:** `100px` horizontal, `120px` vertical. Generous whitespace is part of the premium feel.
- **No grid** — asymmetric layouts. One element breaks the implied grid in every content slide.

---

## The two-background rule (non-negotiable)

Every slide is either an **act** slide or a **content** slide. No third option.

### Act slide
- Background: `#5E17EB` purple
- Headline: `#FFFFFF` white in Anton
- Use for: title slide, section dividers ("ACT II"), closer, hero / cinematic moments
- Optional decoration: diagonal `--purple-dark` block rotated ~45° in a corner at ~30–40% opacity

### Content slide
- Background: `#F1F2F2` light grey
- Headline: `#000` black in Anton, flanked left by a `<PurpleBar>`
- Use for: everything else (info, evidence, lists, dashboards, architecture, stat, story)
- Cards on content slides: `#FFFFFF` background, `1px solid rgba(0,0,0,0.12)` border, `4px solid #5E17EB` left border

**Yellow is an accent on either background — never floor a slide in yellow.**

---

## The FlightHUD strip (every slide)

A horizontal HUD strip sits at the bottom of every slide:

- Progress bar (slide N / total)
- Flight phase tag (PRE-FLIGHT · TAKEOFF · CLIMB · CRUISE · DESCENT · FINAL · LANDED)
- Four readout cells: ALT (ft) · SPD (kt) · HDG (°) · FUEL (%)
- Citation slot (left-aligned, JetBrains Mono, dim)
- Flight ID (right-aligned, e.g. "FLIGHT FH-YUV-AI")
- Slide number (right-aligned, Anton, 22px, zero-padded)

Component lives at `references/components/FlightHUD.tsx`. The default flight-status function (`defaultFlightStatus(n, total)`) maps slide index to phase across a 23-slide journey. Override `status` for custom decks.

The HUD tone (`content` vs `purple`) auto-adapts to the slide's background.

---

## Slide types

### Title / opening (act)

- Massive Anton wordmark or talk title, 280–360px, white on purple.
- Small JetBrains Mono eyebrow above (e.g. `PRE-FLIGHT · MAY 12 2026 · TLV`).
- One supporting line in Inter 400 below the headline.
- Optional `<CompassDial>` or `<AltimeterDial>` decoration in a corner.
- FlightHUD at bottom, tone="purple".

### Section divider (act)

- Anton headline ~200px ("ACT II / EVIDENCE").
- A single Anton subline in yellow OR a yellow highlight span.
- Diagonal `--purple-dark` decoration in a corner.

### Content (info, body)

- `<PurpleBar>` to the left of every H1 (96–140px).
- H1 in Anton uppercase black.
- Body in Inter 400, 22–28px, max 60ch wide.
- Cards laid out in a 2- or 3-column asymmetric grid.

### Stat (big number)

- One enormous Anton number (200–280px), `<CounterUp>` animated.
- Above: JetBrains Mono eyebrow with tracking 0.3em (e.g. "AVERAGE WIN RATE · MAY 2026").
- Below: Inter 400 caption with the supporting context (one line max).

### Quote / pull-quote (content)

- Anton uppercase headline in `clamp(80px, 8vw, 140px)`.
- One word highlighted with yellow `box-decoration-break: clone` span.
- Attribution in Inter 500, 18px, color `rgba(0,0,0,0.55)`.

### Closing / CTA (act)

- Single line of Anton white on purple.
- Pill CTA — black background, white Anton text, `border-radius: 999px`, padding `1.25rem 2.5rem`.
- Linktree URL OR a single QR code centered.
- Brand watermark (`logo-rectangle-wordmark.png`) bottom-right.

---

## Signature video banner — mandatory on landing sites

Every landing page or marketing site opens with a cinematic product-demo video banner. **Not optional.** "Hero with static text and a stock image" is banned.

### What the video is

- A standalone Hyperframes-compatible HTML composition at `public/demo/index.html`.
- Embedded as a full-width 16:9 `<iframe>` at the top of the page, above the traditional hero section.
- Self-looping in the browser via `onComplete → rebuild → play(0)` — **never** `repeat: -1` (breaks Hyperframes capture).
- Renderable to MP4 later via `npx hyperframes render`.

### 6-scene narrative arc (~12–18 seconds total)

1. **Logo slam** (~1s) — giant Anton wordmark + triangle mark slams in on off-white. Establishes brand.
2. **Headline hold** (~2s) — massive black scene with yellow/pink Anton headline stating the core promise. Subtitle in white Anton below.
3. **Device interaction** (~4s) — iPhone or MacBook mockup with a **LIVE product dashboard inside it**. A pink cursor enters, hovers over multiple interactive elements with row highlights, then clicks. The product transitions to a detail view. Cursor continues interacting. This is the signature moment.
4. **Evidence cascade** (~3s) — full-screen cascade of 3–4 evidence/feature cards entering with staggered `gsap.from({ opacity: 0, y: 40, scale: 0.96 })` at 150ms intervals.
5. **Climactic payoff** (~2.5s) — massive headline reveal with the core stat, accompanied by 2–3 counters animating up from 0 (`onUpdate` callbacks, `power2.out` ease).
6. **Pink/purple flood CTA** (~2s) — full brand-color background, enormous Anton headline ("Stop missing what matters" / "Start flying"), solid black pill CTA. Closes the narrative.

### Device mockup specifics

- **iPhone** for consumer / vertical product stories: pure CSS frame at 540×1100px container, 72px border-radius, 18px dark padding, inner screen at 54px radius, notch as absolute-positioned black pill.
- **MacBook** for enterprise / dashboard products: CSS frame with laptop base and screen bezel.
- Inside the device: **real product UI rendered in HTML, not screenshots**. The cursor actually interacts with elements.

### Cursor choreography

The cursor is the emotional vehicle. Treat it like a character.

- Pink (or purple, in Fly High) **teardrop cursor** rotated -45°, off-white inner dot, 38px.
- Entry from bottom-right at 0.5 scale, scaling to 1.0 as it settles.
- **Multiple interactions before the main click** — hover over 2–3 other elements first to establish the scan. Each hover triggers a subtle row highlight.
- **Click cue:** `scale: 0.85` press on cursor, synced `click-ring` element (`80px` circle, brand border) expanding `scale 0.5 → 2.2, opacity 1 → 0` over 0.6s.
- **Cursor continues after the click.** Don't cut to black — show the cursor navigating the result.

### Deterministic loop pattern

```js
let tl = buildTimeline();
tl.eventCallback('onComplete', () => {
  tl.kill();
  tl = buildTimeline();
  tl.play(0);
});
window.__timelines = window.__timelines || {};
window.__timelines['<composition-id>'] = tl;
```

### Scaling to viewport

Author at fixed dimensions (1920×1080 horizontal, 1080×1920 vertical). A `fitToViewport()` function computes `scale = min(innerWidth/1920, innerHeight/1080)` and applies via CSS transform with top-left origin, centered with margins. Re-runs on `resize`.

### React embed

```tsx
export function DemoVideo() {
  return (
    <section aria-label="Product demo" style={{ width: '100%', background: 'var(--yuv-grey)' }}>
      <div style={{ position: 'relative', width: '100%', aspectRatio: '16 / 9' }}>
        <iframe src="/demo/index.html" title="Product demo" loading="eager"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', border: 'none' }} />
      </div>
    </section>
  );
}
```

Mount as the first child of `<main>`, above the traditional hero section.

### Why HTML over MP4

- **Editable in seconds** — no re-render cycle.
- **Crisp at any resolution.**
- **Renders to MP4 on demand** via `npx hyperframes render`.
- **Text is live** — A/B test copy without re-rendering.
- **Lives with the code.** No "which folder was that MP4 in?"

---

## Watermarking

Every deck has the brand watermark (`logo-rectangle-wordmark.png`) in the bottom-right corner. Rules:

- Width ~120–180px on a 1920px canvas.
- Margin ~3% of canvas (~60px from right and bottom edges).
- Never stretch — preserve aspect ratio.
- Opacity 100% on grey content slides. 80% on purple act slides (the colored wordmark has enough internal contrast).
- Position: `position: absolute; bottom: 32px; right: 32px;`.

---

## Self-check for slide decks

1. Every slide is either act (purple) or content (grey) — no third background.
2. Yellow appears only as accent (highlight span, underline, instrument tag) — never as a slide background.
3. `<PurpleBar>` next to every content-slide H1.
4. `<FlightHUD>` at the bottom of every slide.
5. Watermark in bottom-right.
6. Anton headlines are UPPERCASE with ``0` default, `-0.01em` only at hero size (≥ 180px) letter-spacing.
7. Line-height ≥ 1.0 on any multi-line Anton headline with a yellow highlight span.
8. `<YellowUnderline>` anchored under a specific word, never decorative.
9. Cards on grey: white bg + 1px border + 4px purple left border.
10. Final / closing slide has Linktree URL (or QR) and watermark.
