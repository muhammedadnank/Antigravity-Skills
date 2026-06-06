# Typography — full system

Mandatory type rules for English, Hebrew, and bilingual surfaces.

---

## English stack

| Role | Family | Where |
|---|---|---|
| Display / headlines | **Anton** | h1, h2, h3, section titles, pull quotes, big stats, CTA labels, wordmarks |
| Body / UI | **Inter** | paragraphs, lists, form fields, buttons (non-display) |
| Mono / readouts | **JetBrains Mono** | eyebrows, citations, instrument readouts, chip labels, code |

### Anton rules

- **Always UPPERCASE** (use `text-transform: uppercase` in CSS). Anton renders title case poorly because it's a condensed display face.
- **Letter-spacing default `0` (normal).** Anton is already condensed — negative tracking pushes letters into each other, especially inside yellow `box-decoration-break: clone` spans, where it reads as a wall of crammed glyphs. **Never tighter than `0` by default.** Only at extreme hero sizes (≥ 180px) and only when measured, drop to `-0.01em` max. The earlier negative-tracking rule was wrong; this is the correction.
- **Inside yellow highlight spans:** add slight POSITIVE tracking — `letter-spacing: 0.01em` to `0.015em` — and use em-based padding (`padding: 0.08em 0.4em`) so the box has breathing room around each letter and scales with the font size.
- **Line-height `1.0`–`1.05`.** Never below `1.0` when a highlight span sits inside (descenders get eaten).
- **Single weight** — Anton ships only one weight. Don't try to bold it via `font-weight`.
- **Size range** — never below 16px in body. Anton at small sizes is illegible. For section eyebrows, use JetBrains Mono instead.
- **One Anton element per slide / section.** Two or more big Anton elements stacked (e.g. a headline plus a row of stat tiles all in Anton) make the surface read like a wall of thick type. Use Anton for the hero only; supporting numbers and labels go in Inter 900 or JetBrains Mono 700.

### Inter rules

- Weights 400 / 500 / 600 / 700 / 900. Use 400 for body, 500–600 for UI labels, 700 for emphasis, 900 only as a fallback display.
- Line-height `1.5` for body, `1.3` for tight UI lists, `1.2` for small headlines.
- Letter-spacing default (`normal`) for body. Don't apply negative tracking to Inter — that's Anton's territory.

### JetBrains Mono rules

- Use for: section eyebrows ("PRE-FLIGHT", "EVIDENCE", "CHAPTER 3"), data readouts, citations under HUD, chips, inline code.
- Always tracking `0.2em`–`0.3em` and weight 700 when used as a label.
- Body text mono is banned — leave it for atmosphere/data only.

---

## Hebrew stack

| Role | Family |
|---|---|
| Display / headlines | **Rubik** (weights up to 900) |
| Body / UI | **Assistant** (400 / 500 / 600 / 700) |

### Hebrew page setup

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="UTF-8">
    <!-- fonts -->
  </head>
  <body>...</body>
</html>
```

### Logical CSS — mandatory on Hebrew pages

Use logical properties instead of physical ones:

| Physical (avoid) | Logical (use) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `border-left` | `border-inline-start` |
| `border-right` | `border-inline-end` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |

With logical properties, the same CSS works in LTR and RTL — the "start" side flips automatically.

### Rubik rules

- Weight 900 for major display. 700 for section heads. 500–600 for UI.
- Letter-spacing default — Hebrew doesn't tolerate the negative tracking Anton uses.
- Line-height `1.05`–`1.15` for headlines. Hebrew glyphs have less vertical reach, so they can run tighter than Anton.

### Assistant rules

- Same weights / use as Inter. Line-height `1.5` for body.

---

## Bilingual stack

Stack both fonts in the variable. The browser picks per glyph automatically.

```css
:root {
  --yuv-font-display: 'Anton', 'Rubik', system-ui, sans-serif;
  --yuv-font-body:    'Inter', 'Assistant', system-ui, sans-serif;
  --yuv-font-mono:    '"JetBrains Mono"', '"SF Mono"', ui-monospace, Menlo, monospace;
}
h1, h2, h3, .display {
  font-family: var(--yuv-font-display);
  text-transform: uppercase;       /* Latin only — Hebrew unaffected */
  letter-spacing: 0;               /* Anton is condensed — never negative by default */
  line-height: 1.0;
}
```

Anton ignores `font-weight`. Rubik respects it. So if your headline mixes Latin and Hebrew, set `font-weight: 900` — Latin Anton uses its single weight, Hebrew Rubik picks the 900 face. Both look display-correct.

### Bilingual content rule (battle-tested)

**Never stack EN + HE side-by-side or in adjacent positions.** Always use the toggle pattern in `lessons-learned.md` § Bilingual toggle.

---

## Google Fonts — one link to rule them all

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;500;700&family=Rubik:wght@400;500;600;700;800;900&family=Assistant:wght@400;500;600;700&display=swap" rel="stylesheet">
```

For English-only projects, drop Rubik + Assistant. For Hebrew-only, drop Anton + Inter. When in doubt, load all five — total uncached weight ~50KB, trivial.

---

## Type-scale reference

### Slide deck canvas (1920×1080)

| Role | Size | Family |
|---|---|---|
| Act-slide hero | 280–360px | Anton |
| Content-slide H1 | 96–140px | Anton |
| Content-slide H2 | 56–72px | Anton |
| Eyebrow above H1 | 13–14px tracking 0.3em | JetBrains Mono |
| Body | 22–28px | Inter |
| Caption / cite | 13–15px | Inter or JetBrains Mono |
| Big stat | 200–280px | Anton |
| HUD readout | 16px | JetBrains Mono |

### Web (1440px max-width)

| Role | Size | Family |
|---|---|---|
| Hero H1 | `clamp(4rem, 9vw, 10rem)` | Anton |
| Section H2 | `clamp(2.5rem, 5vw, 5rem)` | Anton |
| Card title | `clamp(1.5rem, 2.5vw, 2.5rem)` | Anton |
| Body | 18px | Inter |
| Small / caption | 14px | Inter |
| Eyebrow | 11–13px tracking 0.2–0.3em | JetBrains Mono |

---

## Banned

- Serif fonts as defaults (Garamond, Times, Playfair, Lora).
- Script / handwritten fonts.
- `system-ui` / OS default stack.
- Comic Sans (obvious but worth saying).
- Inter as a display font (don't bump it up to 900 to substitute Anton — load Anton).
- Anton in body (illegible at small sizes — use Inter).
- Two display headlines stacked (see `lessons-learned.md` § 3).
