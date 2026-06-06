# Design Notes — Scroll-Driven Landing Page

Defaults align with the `yuv-design-system` skill (Fly High purple by default). **A project-specific brand system always
wins** — only fall back to these when no brand is specified.

## Typography

| Language | Display / Headlines | Body / UI |
| -------- | ------------------- | --------- |
| English  | **Anton** (400)     | **Inter** (400 / 600 / 700) |
| Hebrew   | **Rubik** (900)     | **Assistant** (400 / 600) |

- Hero headline: 48px → 160px responsive (`clamp(48px, 8vw, 160px)`).
- Section headings: 40px → 110px (`clamp(40px, 5.4vw, 110px)`).
- Body: 17–22px responsive, line-height 1.6.

## Palette

| Token        | Hex       | Use                                        |
| ------------ | --------- | ------------------------------------------ |
| `--pink`     | `#ff3da6` | CTAs, primary accents, scroll-cue lines    |
| `--yellow`   | `#ffd24a` | Section headlines, secondary accents       |
| `--bone`     | `#f5f0d0` | Body text on dark, hero headline           |
| `--bg`       | `#0a0a12` | Page background (near-black, not pure #000) |
| `--ink`      | `#14141c` | CTA text colour on pink                    |

**Do NOT use** `#FFFFFF` (use `--bone`), `#000000` (use `--bg`), or 8–12px border radii
(use `0` or `999px`).

## Hero overlay

- Subtle. The video frame IS the hero — text just labels it.
- Vignette: `radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.55) 100%)` plus
  top/bottom darken bands.
- Headline gets a soft text-shadow `0 10px 40px rgba(0,0,0,0.6)` so it reads over any frame.

## Motion

- Scroll is the primary motion device. Don't auto-play other animations in the hero — it
  fights the scroll-frame.
- Scroll-cue line at the bottom of the hero: 1px line that scales 0.2 → 1 with a 1.8s easing
  loop. Disappears after first scroll (`opacity: 0` once `scrolledIntoStage > 100`).
- Below-hero sections: GSAP-style reveals are fine (scroll-triggered fade + 20px lift). Keep
  durations 0.5–0.8s and easing soft (`power3.out`).

## Layout

- Hero is full-bleed (`100vw × 100vh`).
- Below-hero sections: padding `18vh 8vw`, max-width on text columns `62ch`.
- Sharp lines between sections — a 1px `rgba(245, 240, 208, 0.08)` divider.

## Hebrew adjustments

```html
<html lang="he" dir="rtl">
```

```css
body { font-family: "Assistant", sans-serif; }
.headline { font-family: "Rubik", sans-serif; font-weight: 900; }
.section h2 { font-family: "Rubik", sans-serif; font-weight: 900; }
.cta { font-family: "Rubik", sans-serif; font-weight: 900; }
```

Keep the same palette + scroll mechanic.
