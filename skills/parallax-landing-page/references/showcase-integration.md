# Showcase Integration — adding a new landing to an existing project

Use this when the target folder already has an `index.html` (hub) and at least one other landing (e.g. `github.html` + `lion.html`). You're not creating from scratch — you're growing what's there.

There are four edits, all small. Do them in this order so the user can preview after each step if they want.

## 1. Add a card to `index.html`

Inside `<div class="hub-cards">`, add a new `<a class="hub-card {{slug}}">` block alongside the existing cards. The grid is already `repeat(3, 1fr)` and collapses gracefully — you don't need to touch it.

Pattern (copy and adapt):

```html
<a href="{{slug}}.html" class="hub-card {{slug}}">
  <div class="hub-card-bg" style="background-image: url('{{slug}}/frame-{{mid}}.jpg');"></div>
  <span class="dot"></span>
  <span class="hub-card-arrow">Enter →</span>
  <div class="hub-card-content">
    <span class="kicker">{{NN}} — {{CATEGORY}}</span>
    <h2>{{HEADLINE_LINE_1}}<br />{{HEADLINE_LINE_2}}</h2>
    <p class="script" style="color: var(--{{accent}});">{{HANDWRITTEN_LINE}}</p>
  </div>
</a>
```

Notes:
- `{{mid}}` is the middle frame number (e.g. `121` for a 241-frame clip) — gives the card a more visually arresting still than frame-001.
- `{{NN}}` is the position in the showcase: `01`, `02`, `03`, etc. Match the order they appear.
- `{{CATEGORY}}` is a one-word taxonomy (Product, Wild, Speed, Story, Field, etc.).
- The `style="color: var(--{{accent}});"` on the handwritten line ties the card to its landing page's accent color.

**Also bump the hub copy** to reflect the new count:

```html
<div class="hub-eyebrow">{{N}} Stories · One Scroll</div>
```

```html
<span class="script">{{n}} short films, one page each.</span>
```

Spell `N` as a word ("Three", "Four", "Five") to match the existing typography rhythm.

**Add the preload link** in `<head>`:

```html
<link rel="preload" as="image" href="{{slug}}/frame-{{mid}}.jpg" />
```

## 2. Add a dot accent style to `style.css`

If the new landing uses an existing accent color (`gold`, `amber`), reuse the dot rule. If it's a new color, add both the variable and the dot rule.

Add the color to `:root` (next to the existing `--accent`, `--gold`, `--amber`):

```css
--{{newcolor}}: #HEXVAL;
```

Add the dot rule right after the existing `.hub-card.lion .dot` / `.hub-card.hope .dot` lines:

```css
.hub-card.{{slug}} .dot {
  background: var(--{{newcolor}});
  box-shadow: 0 0 0 4px rgba(R, G, B, 0.18);
}
```

The RGB triplet should match the hex. (E.g., `#ff8a3d` → `255, 138, 61`.)

And if you want the handwritten lines on that landing to use this color, also add:

```css
.script.{{newcolor}} { color: var(--{{newcolor}}); }
.cta.{{newcolor}}    { border-color: var(--{{newcolor}}); color: var(--{{newcolor}}); }
.cta.{{newcolor}}:hover { background: var(--{{newcolor}}); color: var(--bg); }
```

## 3. Add the new landing to every existing nav

In `index.html`, `github.html`, `lion.html`, and any other landing, find the `.nav-links` block and add:

```html
<a href="{{slug}}.html">{{Title}}</a>
```

On the new landing's own page, the link gets `class="active"`. On every other page, no class.

Maintain a stable order across all pages — easiest is alphabetical or "by show-order" (i.e. matching the hub card order). Either is fine; just be consistent so the nav doesn't jitter as the user clicks around.

## 4. Chain the previous landing's final scene

In the immediately previous landing (the one with the highest existing number), update the `end-actions` block inside its scene 5 to add a chain link to the new landing.

Before:
```html
<div class="end-actions">
  <a class="cta gold" href="...">Visit Midbarium</a>
  <a class="cta" href="...">Open in Maps</a>
  <a class="cta" href="index.html">← Back to showcase</a>
</div>
```

After:
```html
<div class="end-actions">
  <a class="cta gold" href="...">Visit Midbarium</a>
  <a class="cta" href="...">Open in Maps</a>
  <a class="cta" href="{{slug}}.html">Next: {{Title}} →</a>
  <a class="cta" href="index.html">← Back to showcase</a>
</div>
```

On the new landing's own scene 5 CTA block, end with `← Back to showcase` and (if appropriate) a chain forward to whatever you'd want next.

## Verification checklist

After all four edits, the user should be able to:

1. Open `index.html` → see N cards in the grid, all with the right backgrounds and accent dots.
2. Click each card → land on the right page, with the loader title matching.
3. Use the nav from any page → reach any other page; the active page is underlined.
4. Scroll to the end of any non-final landing → see a `Next →` CTA pointing to a real page.
5. Scroll to the end of the new landing → see the back-to-showcase CTA.

If any of those breaks, you missed an edit. Re-check `nav-links` parity across files.

## Common slips to avoid

- **Forgetting to add the slug to the preload list in index.html.** Cards without a preload still load, just a beat later.
- **Mixing accent colors on a single card.** The card BG accent (dot + script color) should match the landing's interior accent — otherwise the hub feels disconnected from the page.
- **Reusing a frame number that's the wrong padding.** Always pad to 3 digits (`frame-073.jpg`, not `frame-73.jpg`).
- **Forgetting to set `class="active"` on the current page's nav link.** Subtle but breaks the "where am I" affordance.
- **Adding a new accent variable but forgetting the `.script.<name>` and `.cta.<name>` rules.** The page renders but the accent never appears anywhere except the dot.
