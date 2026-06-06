# Lessons learned — hardened patterns

Production-tested patterns and the anti-patterns they replace. Each entry below cost a real iteration in a real session. Read before starting any web or visual output.

---

## §1. Bilingual = toggle, never side-by-side

**Anti-pattern:** Showing English headline + Hebrew headline stacked or in adjacent columns. Anton at `8vw` + Rubik 900 at `5–6vw` visually collide because line-heights below 1.0 cause descenders to invade the next ascender row. Users see "the fonts are way too thick and override each other."

**Pattern:** Language toggle. One language visible at a time. `data-lang="en"` / `data-lang="he"` attributes on every translatable element + a universal show/hide rule + a state handler.

### HTML

```html
<div class="lang-toggle" role="group" aria-label="Language toggle">
  <button class="lang-btn active" data-lang-set="en" aria-label="English"><span>🇺🇸</span>EN</button>
  <button class="lang-btn"        data-lang-set="he" aria-label="עברית"><span>🇮🇱</span>HE</button>
</div>

<h1>
  <span data-lang="en">Pick the effect, not the code.</span>
  <span data-lang="he">בחר את האפקט, לא את הקוד.</span>
</h1>
```

### CSS

```css
html:not([lang="he"]) [data-lang="he"] { display: none !important; }
html[lang="he"]       [data-lang="en"] { display: none !important; }

[data-lang="he"] { direction: rtl; unicode-bidi: embed; }
[data-lang="he"]:where(p, span:not(.flag), em, strong) {
  font-family: 'Assistant', 'Inter', sans-serif;
}
h1 [data-lang="he"], h2 [data-lang="he"], h3 [data-lang="he"], h4 [data-lang="he"] {
  font-family: 'Rubik', sans-serif;
  font-weight: 900;
}

.lang-toggle {
  display: inline-flex; gap: 0; padding: 2px;
  background: rgba(10,10,10,0.05);
  border: 1px solid rgba(10,10,10,0.1);
  border-radius: 999px;
}
.lang-btn {
  font-family: 'Anton', sans-serif;
  font-size: 12px; letter-spacing: 0.10em; text-transform: uppercase;
  padding: 5px 12px; border-radius: 999px;
  background: transparent; border: none; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px;
}
.lang-btn.active { background: var(--yuv-purple, #5E17EB); color: #fff; }
```

### JS

```js
const TITLES = {
  en: 'Yuval Avidani — Let’s Fly High',
  he: 'יובל אבידני — בואו נטוס גבוה',
};

function setLang(lang) {
  document.documentElement.lang = lang;
  document.title = TITLES[lang] || TITLES.en;
  document.querySelectorAll('[data-lang-set]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.langSet === lang);
  });
  try { localStorage.setItem('yuv-lang', lang); } catch {}
}

document.querySelectorAll('[data-lang-set]').forEach(btn => {
  btn.addEventListener('click', () => setLang(btn.dataset.langSet));
});

setLang(localStorage.getItem('yuv-lang') || document.documentElement.lang || 'en');
```

**Don't forget `document.title`** — leaving the tab title in English is the most common "half-built bilingual" giveaway.

**Mobile rule:** the toggle must be duplicated into the always-visible mobile cluster, not just inside the hamburger menu. Otherwise mobile users need one extra interaction to switch language.

---

## §2. Mobile = hamburger, always, at ≤880px with > 6 nav items

**Anti-pattern:** A flat horizontal nav with `flex-wrap: wrap`. On desktop fine; on mobile it eats 50% of the viewport.

**Pattern:** Hamburger menu for `max-width: 880px` whenever nav has more than 6 items.

```html
<header class="topbar">
  <a class="brand" href="/">YUV.AI</a>
  <button class="hamburger" aria-label="Menu" aria-expanded="false">☰</button>
  <nav class="nav">
    <a href="#about">About</a>
    <a href="#work">Work</a>
    <a href="#course">Course</a>
    <a href="#talks">Talks</a>
    <a href="#blog">Blog</a>
    <a href="#contact">Contact</a>
    <div class="lang-toggle">...</div>
  </nav>
</header>
```

```css
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; }
.hamburger { display: none; background: none; border: none; font-size: 24px; cursor: pointer; }
.nav { display: flex; gap: 22px; align-items: center; }

@media (max-width: 880px) {
  .hamburger { display: block; }
  .nav { position: absolute; top: 64px; left: 0; right: 0; flex-direction: column; align-items: flex-start; gap: 14px; padding: 24px; background: var(--yuv-grey); border-top: 1px solid rgba(0,0,0,0.08); transform: translateY(-110%); transition: transform 220ms ease; }
  .nav.open { transform: translateY(0); }
}
```

```js
const hb = document.querySelector('.hamburger');
const nav = document.querySelector('.nav');
hb.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  hb.setAttribute('aria-expanded', String(open));
});
```

---

## §3. One display headline per section — never two stacked

Stacking two display-weight fonts (e.g. Anton h1 + Rubik h1) with `line-height < 1.0` causes overlap. If you need a subhead, make it 50% of the headline size and **don't** use a display font for it.

---

## §4. Never assign HTML strings as element content with variables

Use `el.textContent = value` for plain text. Use `createElement` + `appendChild` for structured content. Reserve direct HTML-string assignment for compile-time literal strings only. Variable HTML assignment is an XSS hole the moment a variable can take user data — and modern browsers' security hooks rightfully block it.

---

## §5. Spec-driven content — zero hallucination

When the user says "add a CTA for X" or "embed link to Y":

- **WebFetch** for HTML-static pages (blogs, docs, GitHub).
- **`curl`** for API endpoints or raw HTML.
- **Claude-in-Chrome** for JS-rendered SPAs (Teachable, Kajabi, learn.*, builder.io, practical.yuv.ai, most modern landing-page builders).

If WebFetch returns suspiciously thin output (< 500 chars, only `<title>` and meta), it's an SPA — re-route to Claude-in-Chrome. **Don't bridge gaps with plausible-sounding invention.** If a field isn't on the page, write "not on page" and ask.

---

## §6. Mobile-first responsive is a baseline check, not polish

Before declaring any frontend work done:

1. Resize the preview to 375×812 (iPhone size).
2. Screenshot.
3. Verify: nav fits, no horizontal text overflow, headlines readable, grid collapses correctly.

If any of those fail, fix and re-screenshot. This is a 30-second check that prevents shipped bugs.

---

## §7. IntersectionObserver for catalogs with > 8 GSAP demos

Multiple GSAP timelines running at 30fps simultaneously will cook the CPU. Pause off-screen demos:

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    const tl = e.target.__tl;
    if (!tl) return;
    if (e.isIntersecting) tl.play();
    else tl.pause();
  });
}, { threshold: 0.15 });
document.querySelectorAll('.stage').forEach(s => observer.observe(s));
```

Each stage stores its timeline at `stage.__tl = tl`. Standard pattern.

---

## §8. `e.stopPropagation()` on inner clickable elements

A clickable card with a clickable child (e.g. a copy-to-clipboard chip inside a card link) causes both the inner handler AND the parent navigation to fire. Stop propagation on the inner:

```js
chip.addEventListener('click', (e) => {
  e.preventDefault();
  e.stopPropagation();
  navigator.clipboard.writeText(value);
  // toast...
});
```

---

## §9. Effect-ID copy chip

Every browse-and-pick interface (catalog, design system, component library) gets a copyable identifier on every item:

- Pink/yellow/purple chip with monospace font.
- Click to copy. Toast confirmation.
- `e.stopPropagation()` if nested inside a card link.

```html
<button class="chip" data-copy="effect.purple-bar.v1">
  <span>effect.purple-bar.v1</span>
  <i class="ph ph-copy"></i>
</button>
```

```css
.chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  padding: 4px 10px;
  background: var(--yuv-yellow);
  color: #000;
  border: 1px solid #000;
  border-radius: 0;
  cursor: pointer;
  display: inline-flex; gap: 8px; align-items: center;
}
```

---

## §9a. Anton letter-spacing — DEFAULT TO ZERO, never negative

**Anti-pattern (real production miss):** setting Anton at `letter-spacing: -0.03em` to `-0.04em` because "headlines feel tighter that way." Anton is already a condensed display face. Layering negative tracking on top makes letters touch — especially visible inside yellow `box-decoration-break: clone` spans, where the highlight box reads as a wall of crammed glyphs. Users describe it as "the type feels too thick" without being able to name the cause.

**Pattern:**

```css
/* default Anton */
.display { font-family: 'Anton', sans-serif; text-transform: uppercase; letter-spacing: 0; line-height: 1.0; }

/* only at hero size (≥ 180px), only when measured */
.display-hero { letter-spacing: -0.01em; }   /* max — never tighter */

/* yellow highlight span: ALWAYS positive tracking + em-based padding */
.highlight {
  display: inline-block;
  background: #FFEC00; color: #000;
  padding: 0.08em 0.4em;          /* em-based — scales with font size */
  letter-spacing: 0.01em;         /* slight POSITIVE tracking inside the box */
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
```

**Detection:** any Anton CSS with `letter-spacing: -0.0[234]em` is wrong. Replace with `0` (default) or `-0.01em` (hero only). Any `.highlight` with pixel padding instead of em padding is wrong at hero sizes.

---

## §9b. One Anton element per slide / section

**Anti-pattern:** A slide with a big Anton headline AND a row of big Anton stat tiles (e.g. headline + `1.` / `ON DEMAND` / `/SKILLS.` / `∞` all in Anton). Five Anton elements stacked = visual brick wall. The user can't name what's wrong; they just say "too thick."

**Pattern:** Anton appears once per slide — as the hero. Supporting numbers and labels render in:
- **Inter 900** at the same large size — holds up at hero scale without condensed-display heaviness.
- **JetBrains Mono 700** for instrument-style readouts (HUD cells, big numbers with monospace character).

**Detection:** count Anton elements on a slide. If > 1, decide which one is the hero and downgrade the rest.

---

## §10. Scope creep on catalogs — build comprehensive on first pass

When the user asks for "a catalog of effects" or "a showcase of components", build comprehensive immediately. The proven 18+ section structure for a catalog site:

> Captions / Markers / Cards / Devices / Magic / 3D / Themes / Transitions / Text / Charts / SFX / Layouts / Features / GSAP / Prompts / Scenarios / Tech / Skills / Connect / Course

Building < 10 sections first means re-iterating 3 times to get to "comprehensive". Plan for 18+ from minute 1.

---

## §11. SSL cert provisioning impatience on GitHub Pages custom domain

If the GH Pages cert state stays at `none` for > 15 min after DNS propagates correctly, toggle the custom domain off and on to kick the Let's Encrypt validation flow:

```bash
gh api -X PUT /repos/{owner}/{repo}/pages -f "cname="
sleep 5
gh api -X PUT /repos/{owner}/{repo}/pages -f "cname=<custom-domain>"
```

Cert lands within 15 min after the toggle. Don't wait the rumored 24 hours.

---

## §12. Per-skill install command, not per-repo

If a skills repo has many skills and the user wants one, use sparse-checkout to install just that one:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/<owner>/<repo> /tmp/x \
  && cd /tmp/x && git sparse-checkout set skills/<skill-name> \
  && mkdir -p ~/.claude/skills && cp -R skills/<skill-name> ~/.claude/skills/ \
  && rm -rf /tmp/x
```

`npx skills add <repo>` shows an interactive checkbox list and forces a manual pick — bad UX for "I want this one specific skill".

---

## §13. Hero = real Hyperframes-compatible composition

For any major site, the hero section should use real Hyperframes `data-*` attributes (`data-composition-id`, `data-start`, `data-duration`, `data-width="1920"`, `data-height="1080"`) on the stage element. The site itself becomes a Hyperframes artifact — `hyperframes render` on the same code produces an MP4 promo. Two outputs (web + video) from one source.

---

## §14. Anton + yellow span = `line-height ≥ 1.0`

When an Anton headline at a large size contains an inline-block yellow highlight span (`display: inline-block; background: #FFEC00; box-decoration-break: clone`), the highlight box eats the previous line's descenders if `line-height < 1.0`. **Bump to 1.0 minimum** whenever the headline is multi-line.

---

## §15. `<YellowUnderline>` always anchors to a specific word

Never floats decoratively. Width matches the underlined word's rendered width. Position absolute, `bottom: -16px`, `left: -4px` of the parent span. If it isn't sized to its word, it looks like a stray underscore.

---

## Quick reference

| Symptom | Pattern |
|---|---|
| EN + HE side-by-side | §1 — toggle |
| Mobile nav wrapping | §2 — hamburger ≤880px |
| Two display headlines stacked | §3 — one per section |
| XSS warning from inserting HTML | §4 — `textContent` / `createElement` |
| Made-up CTA content | §5 — read the page first |
| Mobile broken on ship | §6 — mobile-first baseline check |
| Page CPU pegged at 100% | §7 — IntersectionObserver |
| Card link navigating on inner button click | §8 — stopPropagation |
| Catalog asked to be "bigger" 3 times | §10 — build comprehensive |
| GH Pages cert stuck | §11 — toggle CNAME |
| User wants 1 of many skills | §12 — sparse-checkout |
| Yellow span eating descenders | §14 — line-height ≥ 1.0 |
| Yellow underline looks random | §15 — anchor to specific word |
