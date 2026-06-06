# Neon mode — the YUV.AI default palette

The everyday YUV.AI brand. Use for **web, apps, games, dashboards, social images, posters, AI tools, profile/about pages** — basically anything that isn't a slide deck. Hot pink as the lead, neon cyan as the electric counterpoint, white or rich black as the canvas. Tavus-inspired confidence; YUV.AI flight throughline.

This is the brand chapter most YUV.AI surfaces live in. Decks (Fly High purple/yellow/grey) are the exception, not the rule.

---

## Tokens

```css
:root {
  /* Brand */
  --yuv-pink:       #FF1464;   /* primary thread — CTAs, brand accents, hero spans */
  --yuv-pink-hot:   #FF0080;   /* high-energy variant — glow shadows, hover states */
  --yuv-cyan:       #00E5FF;   /* electric secondary — data points, focus rings, links */
  --yuv-cyan-edge:  #00FFFF;   /* max-neon — small surfaces only, never bodies of text */

  /* Surfaces */
  --yuv-white:      #FFFFFF;   /* canvas (light mode) */
  --yuv-black:      #0A0A0A;   /* canvas (dark mode), text-on-light */
  --yuv-charcoal:   #1A1A1A;   /* secondary text on light, secondary surface on dark */
  --yuv-soft:       #F4F4F6;   /* alt light surface for subtle layering on #FFFFFF */
  --yuv-line:       rgba(255,20,100,0.18);   /* divider lines, faint pink */
  --yuv-line-cy:    rgba(0,229,255,0.22);    /* divider lines, faint cyan */
  --yuv-shadow:     0 0 24px rgba(255,20,100,0.35);   /* pink glow shadow */
  --yuv-shadow-cy:  0 0 24px rgba(0,229,255,0.30);    /* cyan glow shadow */
}
```

JSON form: `references/tokens/palette.json` (Decks tokens for now; Neon tokens to be added on next iteration).

## Canvas — pick one, never grey

Neon mode allows exactly two canvas options. Don't blend them into a grey middle.

| Canvas | Use for | Pair with |
|---|---|---|
| **`#FFFFFF` (light)** | Marketing pages, About/profile pages, lighter dashboards, brochure-style sites | Pink for CTAs and accents, cyan for highlights, charcoal text |
| **`#0A0A0A` (rich black)** | Product UIs, games, dashboards, "premium" surfaces, anything where glow effects matter | Pink hero accents, cyan secondary, white text, pink/cyan glow allowed |

**No `#F1F2F2` greys (that's Decks mode), no `#FAFAF7` off-whites (that's Warm Editorial).** Pure white or rich black. Pick once per project.

---

## Pink, cyan, and the rule of one accent at a time

Pink and cyan are both saturated. If they share equal weight on the same surface, the eye doesn't know where to land. Use them in a **lead + counter** relationship:

| Surface | Lead | Counter |
|---|---|---|
| Hero CTA + body | Pink (CTA fill, "current" highlight) | Cyan (link hover, secondary CTA outline) |
| Data dashboard | Cyan (chart lines, scale highlights) | Pink (hero stat, status callouts) |
| Game UI | Pink (player accents, health) | Cyan (collectibles, energy meters) |
| Form fields | Cyan (focus ring) | Pink (validation errors, "primary" submit) |

If pink dominates the surface, cyan can only appear on small high-attention elements (a focus ring, a hover state, a single data point). If cyan dominates, pink shows up as the human/CTA layer.

**Never have pink AND cyan both at 100% surface area — pick which is lead per screen.**

---

## Glow effects — allowed, in moderation

This is the mode where YUV.AI feels like a neon sign. Glow is welcome, controlled.

### Text glow

```css
.hero {
  color: var(--yuv-pink);
  text-shadow:
    0 0 16px rgba(255,20,100,0.65),
    0 0 32px rgba(255,20,100,0.35);
}
.hero-cyan {
  color: var(--yuv-cyan);
  text-shadow:
    0 0 18px rgba(0,229,255,0.6),
    0 0 36px rgba(0,229,255,0.3);
}
```

### Box glow (cards, CTAs)

```css
.cta-primary {
  background: var(--yuv-pink);
  color: #FFFFFF;
  box-shadow:
    0 0 24px rgba(255,20,100,0.5),
    0 0 48px rgba(255,20,100,0.25);
}
.cta-primary:hover {
  background: var(--yuv-pink-hot);
  box-shadow:
    0 0 32px rgba(255,0,128,0.7),
    0 0 64px rgba(255,0,128,0.35);
}
.card-on-black {
  background: #0A0A0A;
  border: 1px solid var(--yuv-line);
  box-shadow: inset 0 0 0 1px transparent;
  transition: box-shadow 240ms ease;
}
.card-on-black:hover {
  border-color: rgba(0,229,255,0.4);
  box-shadow: 0 0 24px rgba(0,229,255,0.20);
}
```

**Don't double-glow.** Either text-shadow OR box-shadow on a given element, not both. Glow is dramatic — use sparingly, on the hero, primary CTA, and one or two accents per surface. Glow on every element = strip-mall neon, not premium.

### Gradients — pink → cyan ONLY

Only acceptable gradient direction. Small surfaces (text underlines, progress bars, button borders). Never a full-page gradient wash.

```css
.progress { background: linear-gradient(90deg, #FF1464 0%, #00E5FF 100%); }
.underline-grad { background: linear-gradient(90deg, #FF1464, #00E5FF); }
```

---

## Card patterns

### Rich-black surface card

```css
.card {
  background: #0A0A0A;
  color: #FFFFFF;
  border: 1px solid rgba(255,20,100,0.22);
  border-radius: 0;       /* always 0 in YUV.AI; pills are the only other option */
  padding: 32px 36px;
}
.card.lead { border-left: 4px solid var(--yuv-pink); }
.card.electric { border-left: 4px solid var(--yuv-cyan); }
```

### White-surface card

```css
.card-light {
  background: #FFFFFF;
  color: #0A0A0A;
  border: 1px solid rgba(0,0,0,0.08);
  border-left: 4px solid var(--yuv-pink);
  border-radius: 0;
  padding: 32px 36px;
}
```

Same shape across modes — `border-radius: 0`, 4px-stripe left border for "lead" cards. Color of the stripe changes per mode.

---

## CTAs

```html
<!-- Primary, pink-fill pill -->
<a class="cta primary" href="...">START THE CLIMB</a>

<!-- Secondary, cyan-outline pill -->
<a class="cta secondary" href="...">SEE THE DEMO</a>
```

```css
.cta {
  display: inline-flex; align-items: center; gap: 10px;
  font-family: 'Anton', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 16px 32px;
  border-radius: 999px;          /* pill — only allowed radius besides 0 */
  text-decoration: none;
  font-size: 18px;
  transition: transform 180ms ease, box-shadow 240ms ease;
}
.cta.primary {
  background: var(--yuv-pink);
  color: #FFFFFF;
  box-shadow: 0 0 20px rgba(255,20,100,0.45);
}
.cta.primary:hover {
  background: var(--yuv-pink-hot);
  transform: translateY(-1px);
  box-shadow: 0 0 32px rgba(255,0,128,0.6);
}
.cta.secondary {
  background: transparent;
  color: var(--yuv-cyan);
  border: 2px solid var(--yuv-cyan);
}
.cta.secondary:hover { background: rgba(0,229,255,0.08); }
```

---

## Universal Fly High throughline in Neon

These motifs travel from Decks mode INTO Neon mode — the palette changes, the brand DNA doesn't:

### Neon-flavored HUD strip (for product UIs)

A bottom or top status strip with phase tag + readouts, in the Neon palette:

```html
<div class="hud-neon">
  <span class="phase">◉ CRUISE</span>
  <div class="cell"><span class="lbl">USERS</span><span class="val">12,840</span></div>
  <div class="cell"><span class="lbl">SPD</span><span class="val">486 KT</span></div>
  <div class="cell"><span class="lbl">FUEL</span><span class="val">76%</span></div>
  <span class="flight">FLIGHT FH-YUV-AI · 02 / 12</span>
</div>
```

```css
.hud-neon {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 32px;
  background: rgba(10,10,10,0.85);
  border-top: 1px solid var(--yuv-line);
  color: #FFFFFF;
  font-family: 'JetBrains Mono', monospace;
}
.hud-neon .phase {
  font-size: 11px; letter-spacing: 0.3em; font-weight: 700;
  color: var(--yuv-cyan);
  border: 1px solid var(--yuv-cyan);
  padding: 4px 10px;
}
.hud-neon .cell { display:flex; flex-direction:column; padding: 4px 12px; }
.hud-neon .lbl { font-size: 9px; letter-spacing: 0.22em; opacity: 0.6; }
.hud-neon .val { font-size: 15px; font-weight: 700; color: var(--yuv-pink); margin-top: 2px; }
.hud-neon .flight { font-size: 11px; letter-spacing: 0.18em; opacity: 0.55; margin-inline-start: auto; }
```

### Altimeter / progress dial (decoration, sparingly)

Same `CompassDial` / `AltimeterDial` components from Decks mode CAN be re-skinned for Neon — swap the purple stroke for cyan, the yellow needle for pink:

```jsx
<CompassDial heading={287} strokeColor="#00E5FF" needleColor="#FF1464" backgroundColor="#0A0A0A" />
```

Use rarely — the dial is a flourish, not a fixture in Neon mode. Hero / loading screen / "console" surfaces only.

### Phoenix mark + watermark

Same brand-asset rules as the other modes — bottom-right corner of any shareable surface, ~120–180px wide on a 1920 canvas. The phoenix art works against both white and rich-black canvas.

---

## Typography in Neon

Same system fonts as all other modes — Anton uppercase for display (`letter-spacing: 0` default), Inter for body, JetBrains Mono for instrument readouts. The colors change:

| Role | On white canvas | On rich-black canvas |
|---|---|---|
| Hero headline | `#0A0A0A` charcoal OR `#FF1464` pink with glow | `#FFFFFF` white OR `#FF1464` pink with glow |
| Sub-headline | `#0A0A0A` | `#FFFFFF` |
| Body | `#1A1A1A` | `rgba(255,255,255,0.85)` |
| Caption | `rgba(10,10,10,0.55)` | `rgba(255,255,255,0.55)` |
| Mono readout | `#FF1464` pink for emphasised values; `#00E5FF` for secondary | same |
| Link | `#FF1464` underline, hover → `#00E5FF` | same |

The Anton-with-yellow-highlight pattern from Decks mode **doesn't translate** to Neon. In Neon, the punchline word uses a **pink underline** or a **pink background span** (not yellow), with the same `letter-spacing: 0.01em` + em-based padding rule:

```html
<h1>The future has <span class="hl-pink">arrived.</span></h1>
```

```css
.hl-pink {
  display: inline-block;
  background: var(--yuv-pink);
  color: #FFFFFF;
  padding: 0.08em 0.4em;
  letter-spacing: 0.01em;
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
}
```

---

## Anti-patterns specific to Neon mode

- **Pink + cyan + yellow all at once.** That's three accents on one surface — the brand chapter mixes. Pick lead/counter, leave yellow for Decks mode.
- **Multi-hue gradients.** Pink → cyan only. No rainbow, no purple, no blue→green.
- **Soft drop-shadow rounded-corner template cards.** Still banned (it's the AI-slop tell across every mode).
- **Default Tailwind classes.** Same rule. No `slate-*`, `zinc-*`, `indigo-*`, `cyan-500` (use the custom `--yuv-cyan`).
- **Border radius 8–12px.** Same rule. `0` or `999px`. Nothing in between.
- **Glow on every element.** Strip-mall neon — too much. Keep glow on hero / primary CTA / one or two accents per surface.
- **`box-shadow: 0 4px 6px rgba(0,0,0,0.1)` defaults.** Replace with pink or cyan glow, OR omit entirely.

---

## When NOT to use Neon (route to a different mode)

- **A slide deck.** Use Decks (Fly High) — `references/presentations.md`.
- **A Hope / Marcus / bigcats / practical.yuv.ai surface.** Use Warm Editorial — `references/palettes-warm-editorial.md`.
- **Yuval explicitly said "purple", "Fly High palette", "yellow accent", etc.** Honor the explicit override.
- **A non-YUV.AI project.** This whole skill shouldn't be applying. Step back.

---

## Self-check before shipping Neon work

1. Canvas is `#FFFFFF` OR `#0A0A0A` — never a grey middle.
2. Pink is the lead OR cyan is the lead — not both at equal weight.
3. Anton hero with `letter-spacing: 0` default, max `-0.01em` at ≥180px.
4. Glow on hero / primary CTA only — not on every element.
5. Gradients are pink → cyan, small surfaces only.
6. Border-radius `0` or `999px`. No 8–12px corners.
7. Brand watermark in the bottom-right of any shareable surface.
8. Canonical socials + credentials in the footer / About / credits.
9. At least one Fly High throughline motif (HUD, dial, progress, phoenix, "let's fly high" copy) is present.
