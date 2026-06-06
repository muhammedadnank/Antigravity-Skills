# Web & React — frontend deep dive

Patterns specific to browser-rendered output: sites, landing pages, React components, dashboards, web artifacts.

---

## Starter HTML — Fly High landing hero (English)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Let's Fly High — YUV.AI</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --yuv-purple: #5E17EB; --yuv-purple-dark: #3D0DA8;
      --yuv-yellow: #FFEC00; --yuv-grey: #F1F2F2;
      --yuv-white: #FFFFFF;  --yuv-black: #000000;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { background: var(--yuv-grey); color: var(--yuv-black); font-family: 'Inter', sans-serif; line-height: 1.5; }
    .hero {
      min-height: 100vh; display: grid; grid-template-columns: 1.2fr 1fr;
      align-items: center; gap: 64px; padding: 120px 80px;
      max-width: 1440px; margin-inline: auto;
    }
    .eyebrow {
      font-family: 'JetBrains Mono', monospace; font-size: 13px;
      letter-spacing: 0.3em; color: var(--yuv-purple); font-weight: 700;
      margin-bottom: 24px;
    }
    .hero h1 {
      font-family: 'Anton', sans-serif; font-size: clamp(4rem, 9vw, 10rem);
      text-transform: uppercase; letter-spacing: -0.01em; line-height: 1.0;
    }
    .hero h1 .highlight {
      display: inline-block; background: var(--yuv-yellow); color: var(--yuv-black);
      padding: 0 18px; -webkit-box-decoration-break: clone; box-decoration-break: clone;
    }
    .cta {
      display: inline-block; margin-top: 32px;
      padding: 18px 36px; background: var(--yuv-purple); color: var(--yuv-white);
      font-family: 'Anton', sans-serif; text-transform: uppercase; letter-spacing: 0.04em;
      border-radius: 999px; text-decoration: none; font-size: 18px;
    }
    @media (max-width: 880px) {
      .hero { grid-template-columns: 1fr; padding: 80px 24px; }
    }
  </style>
</head>
<body>
  <!-- HYPERFRAMES_VIDEO_SLOT: hero -->
  <section class="hero">
    <div>
      <span class="eyebrow">YUV.AI · LET'S FLY HIGH</span>
      <h1>Build AI<br>that <span class="highlight">actually</span><br>works.</h1>
      <a href="#start" class="cta">Start the climb</a>
    </div>
    <div><!-- right column for visual / 3D / live demo --></div>
  </section>
  <!-- /HYPERFRAMES_VIDEO_SLOT -->
</body>
</html>
```

---

## React + Tailwind preset

```jsx
// tailwind.config.js
const yuv = require('./references/tokens/tailwind.config.js');
module.exports = {
  presets: [yuv],
  content: ['./src/**/*.{ts,tsx,html}'],
};
```

```tsx
import { PurpleBar, YellowUnderline, CounterUp } from './yuv';

export default function HeroSection() {
  return (
    <section className="grid grid-cols-1 md:grid-cols-[1.2fr_1fr] gap-16 min-h-screen items-center px-[5%] max-w-content mx-auto bg-grey">
      <div>
        <span className="font-mono text-[13px] tracking-[0.3em] text-purple font-bold mb-6 block">
          YUV.AI · LET'S FLY HIGH
        </span>
        <h1 className="font-display uppercase tracking-tightest leading-none text-[clamp(4rem,9vw,10rem)]">
          Build AI<br />
          that <span className="inline-block bg-yellow text-black px-[18px]" style={{ boxDecorationBreak: 'clone' }}>actually</span><br />
          works.
        </h1>
        <a href="#start" className="inline-block mt-8 px-9 py-4 bg-purple text-white font-display uppercase tracking-wide rounded-pill no-underline text-lg">
          Start the climb
        </a>
      </div>
      <div>{/* right column */}</div>
    </section>
  );
}
```

---

## Page architecture defaults

| Region | Defaults |
|---|---|
| Topbar / nav | Sticky on desktop, hamburger on mobile (≤ 880px) when > 6 items. Background `var(--yuv-grey)` with `1px solid rgba(0,0,0,0.08)` bottom border. |
| Hero | First child of `<main>`, full-viewport, ALWAYS the signature video banner (`<iframe src="/demo/index.html">`) above the static hero. |
| Sections | `padding-block: 120px` desktop, `64px` mobile. Alternate purple/grey only when the section is meaningfully different — never decoratively. |
| Cards | `border-radius: 0`. Borders `1px solid rgba(0,0,0,0.12)`. Optional `4px solid var(--yuv-purple)` left border on info cards. |
| CTAs | Primary: `bg-purple` (or `bg-pink` in Warm Editorial), white text, Anton uppercase, `border-radius: 999px`. Secondary: bordered `2px solid var(--yuv-black)`, transparent fill. |
| Footer | The canonical social links + brand watermark. See `social-and-links.md`. |

---

## Performance defaults

- **IntersectionObserver** pauses any GSAP timeline whose stage is offscreen (essential for catalogs with > 8 demos).
- **Preconnect** Google Fonts in `<head>`. Don't `@import` from CSS — blocks render.
- **`loading="eager"`** for the hero video banner iframe, `loading="lazy"` for any other below-the-fold media.
- **No `localStorage` access during render** (only on user action or `useEffect`).
- **`will-change` sparingly** — only on elements that actually animate. Overuse cooks the GPU.

---

## Accessibility defaults

- Every `<a>` and `<button>` has a visible focus ring — `:focus-visible { outline: 3px solid var(--yuv-yellow); outline-offset: 4px; }`.
- Body text contrast: AA minimum. Anton at large sizes always passes; small Inter on `--yuv-grey` needs `#000` not `#1A1A1A` to hit AAA.
- All icons get an `aria-label`. All decorative SVGs get `aria-hidden`.
- Language toggle has `role="group"` + `aria-label`.
- Buttons that toggle state expose `aria-expanded`.

---

## Common patterns

### Counter-up on viewport entry

```tsx
import { useEffect, useRef, useState } from 'react';
export function CounterUp({ to, duration = 1400 }: { to: number; duration?: number }) {
  const ref = useRef<HTMLSpanElement>(null);
  const [n, setN] = useState(0);
  useEffect(() => {
    const io = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      const t0 = performance.now();
      const tick = (now: number) => {
        const t = Math.min(1, (now - t0) / duration);
        const eased = 1 - Math.pow(1 - t, 3);   // ease-out cubic
        setN(Math.round(to * eased));
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      io.disconnect();
    }, { threshold: 0.3 });
    if (ref.current) io.observe(ref.current);
    return () => io.disconnect();
  }, [to, duration]);
  return <span ref={ref}>{n}</span>;
}
```

### Sticky purple side accent

```css
.section::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;          /* full height, left side */
  inset-inline-start: 0;       /* RTL-safe */
  width: 8px;
  background: var(--yuv-purple);
}
```

---

## Mobile baseline check (mandatory)

Before shipping any frontend output:

1. Open browser DevTools → device toolbar → iPhone 13 (390×844).
2. Screenshot.
3. Verify nav fits, no horizontal scroll, headlines readable, grid collapses to 1 column, footer fits.
4. Tap the hamburger — does the menu actually open? Does the language toggle work on mobile?

If any check fails, fix and re-verify. Mobile is not polish; it's the baseline.
