# GOLDEN PROMPT — Cinematic Mouse-Scrub Landing Page

A reusable, opinionated template for building premium landing pages where a **hero video is scrubbed by mouse movement** and each section of the page has its own **brand-driven visual identity**. Works for any product, any language, any subject — food, tech, animals, fashion, services.

---

## How to use this template

1. **Drop your assets** into a clean working directory:
   - Hero video (any container — `.mp4`, `.mov`, `.webm`)
   - Logo (SVG strongly preferred, PNG with transparency acceptable)
   - 1–3 product/subject images (JPG/PNG, transparent background ideal)

2. **Fill in the YAML block at the top of the prompt below** (product name, tagline, language, narrative arc).

3. **Paste the whole prompt** (from "PROMPT START" to "PROMPT END") into Claude Code in that directory. Claude will do everything else.

4. **Don't second-guess the rules.** Every constraint below was learned the hard way. They override generic "good code" defaults.

---

## INPUTS — fill these in before pasting

```yaml
PRODUCT_NAME: "<e.g. במבה / Bamba / Hope the Cheetah / Acme CRM>"
TAGLINE: "<the meta-message — e.g. 'it's not a snack, it's lifelong memories'>"
LANGUAGE: "<he | en | ar | es | fr | ja | ... >"          # used for lang/dir + font choice
IS_RTL: "<true | false>"                                   # he/ar/fa = true; everything else = false
HERO_VIDEO_FILE: "<exact filename in cwd — e.g. baby2.mp4>"
LOGO_FILE: "<exact filename — leave blank if none>"
PRODUCT_IMAGE_FILE: "<exact filename — leave blank if none>"
BRAND_CONTEXT: |
  <2–4 sentences describing the brand: era it evokes, who the audience is, the
  emotional core, the visual identity (warm/cool/playful/serious). Claude uses
  this to extract a palette and pick decorative motifs.>
PALETTE: "<optional — comma-separated hexes if you want to override>"
NARRATIVE_ARC: |
  <optional — 5 emotional beats the page should travel through, e.g.
  "longing → joy → nostalgia → contemplation → action". Leave blank to let
  Claude propose one based on BRAND_CONTEXT.>
```

---

## PROMPT START

You are building a single-page Vite + React + TypeScript + Tailwind v3 landing page using the inputs above. Execute every step end-to-end. Do not skip, do not improvise on architecture, do not pick generic stock defaults. Every rule in this prompt is load-bearing.

---

### PHASE 0 — Read the inputs and propose the design

Before writing any code, output a brief plan (≤200 words) covering:
- The extracted **5-color palette** (background, primary accent, secondary accent, supporting tone, ink/text). Extract from the logo and product image if no PALETTE was given. The palette must be **internally cohesive** — all warm OR all cool, never mixed. If the brand is warm (food, nature, nostalgia, animals) → no blues, teals, mints, or cyans. If the brand is cool (tech, finance, medical, sci-fi) → no warm tones except small accents.
- The **typography trinity** (display / body / handwritten-accent) appropriate to LANGUAGE:
  - `he`: Rubik (display) + Assistant (body) + Suez One (accent)
  - `en`: Anton (display) + Inter (body) + Caveat (accent)
  - `ar`: Cairo (display) + Tajawal (body) + Reem Kufi (accent)
  - `es`/`fr`/`it`/`de`: Anton or Bebas Neue (display) + Inter (body) + Caveat (accent)
  - `ja`: Noto Sans JP (display, weight 900) + Noto Sans JP (body) + Yusei Magic (accent)
  - Other → choose three Google Fonts that match the script, with the same display-black/body-clean/handwritten-script roles
- The **narrative arc** — 5 sections that map to BRAND_CONTEXT's emotional journey. Each section is one emotional beat with its own palette flavor and layout pattern (see section library below).

Then proceed to build. Do not ask for confirmation — execute.

---

### PHASE 1 — Asset preparation (the magic step)

**1a. Verify ffmpeg is installed.** Run `which ffmpeg` (or `Get-Command ffmpeg` on Windows). If absent, stop and tell the user to install it.

**1b. Re-encode the hero video with every frame as a keyframe.** Browsers only seek instantly to keyframes; a typical video has one per ~250 frames, which makes mouse-scrub stutter. The all-keyframes encode is the magic that makes the effect feel real:

```bash
ffmpeg -y -i <HERO_VIDEO_FILE> -g 1 -keyint_min 1 -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -an hero.mp4
```

Verify `hero.mp4` exists and is 5–50 MB. If > 50 MB re-run with `-crf 25`; if > 80 MB with `-crf 28`.

**1c. Logo and product image.** If LOGO_FILE is provided, copy it to `public/logo.<ext>`. If PRODUCT_IMAGE_FILE is provided, copy to `public/product.<ext>`.

---

### PHASE 2 — Scaffold the Vite project

```bash
npm create vite@latest site -- --template react-ts
cd site
npm install
npm install lucide-react
npm install -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
mkdir -p public
mv ../hero.mp4 public/hero.mp4
# also move the logo/product image into public/ if present
```

---

### PHASE 3 — Tailwind config

Replace `tailwind.config.js` entirely. Use the extracted palette names: `background` (page bg / ink), `accent` (primary brand color), `accent2` (secondary), `support` (tertiary tone), `cream` (off-white text). Set the fontFamily to match the language's typography trinity.

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: '<extracted ink/dark>',
        cream: '<extracted off-white — NEVER pure #FFFFFF>',
        accent: '<primary brand color>',
        accent2: '<secondary>',
        support: '<tertiary>',
        ink: '<deepest dark>',
      },
      fontFamily: {
        sans: ['<body font>', 'system-ui', 'sans-serif'],
        display: ['<display font>', 'sans-serif'],
        accent: ['"<handwritten font>"', 'cursive'],
      },
    },
  },
  plugins: [],
}
```

---

### PHASE 4 — index.html

Replace entirely. Honor IS_RTL. Always include the favicon link pointing at the logo. Always preconnect to Google Fonts.

```html
<!DOCTYPE html>
<html lang="<LANGUAGE>" dir="<rtl if IS_RTL else ltr>">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/logo.svg" />   <!-- or /logo.png — use what was provided -->
    <link rel="apple-touch-icon" href="/logo.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="<Google Fonts URL for the three chosen fonts>" rel="stylesheet">
    <title><PRODUCT_NAME> — <TAGLINE></title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

### PHASE 5 — index.css

Replace entirely. This is the design system. Every utility is load-bearing:

- `html { scroll-behavior: smooth; }` and `section[id] { scroll-margin-top: 90px; }` so navbar-anchored sections don't get covered by the fixed nav.
- `body` background set to the `background` color (fallback for when the video fails). Cursor `crosshair`. Default font is body sans.
- `.liquid-glass` and `.liquid-glass-strong` — backdrop-blur + saturate + inset-light border + masked gradient edge highlight. The strong variant has a stronger inset glow tinted with the accent color.
- `.glass-pill` — compact rounded pill with the same glass treatment, sized for nav items and small badges.
- `.cta-primary` — the brand CTA button: linear-gradient using accent → accent-shade, accent-color glow shadow that intensifies on hover, slight translate-y on hover.
- `.brand-mark` — small square/circle for tiny logo marks if no SVG is provided.
- `.grid-bg` — subtle 1px grid with radial mask, used as a texture under the dark sections.
- `.reveal` / `.revealed` — IntersectionObserver-driven scroll reveal: `opacity 0 → 1` and `translateY 28 → 0` over 0.9s with `cubic-bezier(0.16, 1, 0.3, 1)`.
- `.scrim-top`, `.scrim-bottom` — gradient overlays for the hero only.
- **Per-section background classes** (one per emotional beat — name them by feeling, not color):
  - `.sun-section` — bright primary-accent gradient with subtle dotted texture; warm equivalent of "opening the bag" energy.
  - `.album-section` — cream paper with radial accent tints and a dotted micro-pattern, masked to fade at edges.
  - `.roast-section` — dark with radial accent glows in two corners and the masked grid texture.
  - `.signal-section` — bold accent-color full bleed (often red/orange/green depending on brand) for the final CTA.
- `.polaroid` — white card with `14px 14px 44px 14px` padding, soft layered shadow, hover lift to `translateY(-6px) rotate(0)`. `.polaroid-tape` is a yellow/accent tape strip absolutely positioned at top-center, rotated -4°, with dashed side hints.
- `.stamp` — dashed-border pill in accent color, uppercase, letterspacing 0.18em.
- `.ribbon` — pricing/popular badge with clip-path triangle bottom, dark drop shadow.
- `.highlight-circle` — hand-drawn-feeling oval drawn via `::after` with a rotated 3px accent-color border around an inline span. Use it around the single most important word in big headings.
- `.peanut-svg` / `.<motif>-svg` — drop-shadow filter for decorative SVG motifs.
- Honor `prefers-reduced-motion: reduce` — disable reveal animation and smooth scroll inside that media query.

---

### PHASE 6 — App.tsx architecture

The architecture is non-negotiable. Get it right the first time:

**6a. Imports.** Pull from `lucide-react`: `Menu, X, ArrowLeft, ArrowRight, ArrowDown, ArrowUp, MousePointer2`, plus 4–8 thematically appropriate icons.

**6b. Reusable components defined inside App.tsx:**
- `useReveal<T extends HTMLElement>()` — IntersectionObserver hook returning a ref; adds `revealed` class on first intersect.
- `GlassCard` — wrapping component with the reveal hook, optional `strong` prop, accepts className.
- `Motif` — a single decorative SVG component themed to the BRAND_CONTEXT (peanut for food, paw for animals, circuit for tech, leaf for nature, etc.). Used as a floating background element.
- `ScrollToTopButton` — fixed `bottom-6 left-6` (RTL) or `bottom-6 right-6` (LTR), appears when `window.scrollY > window.innerHeight * 0.6`, smooth scrolls to top on click, has the `cta-primary` styling with an ArrowUp icon and a short label in LANGUAGE ("לראש" / "Top" / "أعلى" / etc.).

**6c. Mouse-scrub video logic.** Lives in a `useEffect` in App:

```tsx
const videoRef = useRef<HTMLVideoElement>(null);
const stateRef = useRef({ targetTime: 0, isSeeking: false });

useEffect(() => {
  const video = videoRef.current;
  if (!video) return;
  const handleLoaded = () => {
    const mid = video.duration / 2;
    video.currentTime = mid;
    stateRef.current.targetTime = mid;
  };
  const handleSeeked = () => {
    const s = stateRef.current;
    s.isSeeking = false;
    if (Math.abs(s.targetTime - video.currentTime) > 0.01) {
      s.isSeeking = true;
      video.currentTime = s.targetTime;
    }
  };
  const handleMouseMove = (e: MouseEvent) => {
    const s = stateRef.current;
    const duration = video.duration;
    if (!duration || isNaN(duration)) return;
    // LTR: e.clientX / width   — RTL: optionally use 1 - (e.clientX / width) if it feels backwards
    const normalized = e.clientX / window.innerWidth;
    s.targetTime = Math.max(0, Math.min(duration, normalized * duration));
    if (!s.isSeeking) { s.isSeeking = true; video.currentTime = s.targetTime; }
  };
  video.addEventListener('loadedmetadata', handleLoaded);
  video.addEventListener('seeked', handleSeeked);
  window.addEventListener('mousemove', handleMouseMove);
  return () => {
    video.removeEventListener('loadedmetadata', handleLoaded);
    video.removeEventListener('seeked', handleSeeked);
    window.removeEventListener('mousemove', handleMouseMove);
  };
}, []);
```

The `isSeeking` guard is critical — without it, mousemove fires faster than the browser can decode and you get seek-queue overflow.

**6d. Navigation.** Five nav items, each `{ label, target }`. Target is either `'top'` or a section id (`recipe`, `moments`, `family`, `contact` — or whatever the narrative arc names them). The `scrollToSection(target)` function smooth-scrolls to the element (or window.scrollTo for `'top'`), and on mobile closes the menu. The CTA button in the navbar also calls `scrollToSection('contact')` (or whatever the final CTA section's id is).

**6e. Root JSX layout (THIS IS THE Z-INDEX TRAP — DO NOT VIOLATE):**

```tsx
return (
  <div className="relative">           {/* ABSOLUTELY NO bg-* class on this wrapper */}
    <ScrollToTopButton />
    <video ref={videoRef} src="/hero.mp4" muted playsInline preload="auto"
           className="fixed inset-0 h-full w-full object-cover -z-20" />

    <nav className="fixed top-0 inset-x-0 z-50 ...">{/* nav */}</nav>
    {menuOpen && <div className="fixed top-24 inset-x-4 z-40 ...">{/* mobile menu */}</div>}

    <section className="relative h-screen overflow-hidden">{/* HERO — video bleeds through */}</section>
    <section id="<beat-1>" className="<beat-1-section> ...">{/* OPAQUE — own identity */}</section>
    <section id="<beat-2>" className="<beat-2-section> ...">{/* OPAQUE */}</section>
    <section id="<beat-3>" className="<beat-3-section> ...">{/* OPAQUE */}</section>
    <section id="contact"  className="<final-section> ...">{/* OPAQUE — the action finale */}</section>
    <footer className="bg-background py-8 ...">{/* tiny mini-footer */}</footer>
  </div>
);
```

**The outer `<div>` must NOT have a background color.** Tailwind classes like `bg-background`, `bg-cream`, `bg-white` on the outer wrapper paint over the `-z-20` video and the hero scrub stops working. Only `body` has `bg-background` (as a fallback). This is the #1 mistake. Catch it before you ship.

---

### PHASE 7 — Section library (pick 4–5 for the body, after the hero)

The hero takes section 1. Then 4 more sections, each picked from this library and adapted to the narrative arc. Do not repeat the same pattern twice. Each section has its own opaque background — the video bleeds through the hero only.

**Section type A — "Sun" (bright primary accent):**
Big primary-color gradient background. Floating decorative motif SVGs at low opacity. Giant faded ghost number/word in a corner (e.g. founding year at 6% opacity, 260px). Headline panel: contrasting cream-tinted rounded card with a strong shadow — heading inside, accent-color script word at -2° rotation as eyebrow, big display-black headline ending in a `.highlight-circle` word. Three "stat cards" below in a row, each cream rounded-[28px] with a different slight rotation (-1.5°, 0.8°, -0.6°), each containing a massive display-black accent2 numeral (88-110px), a small label badge top-right, descriptive body text, footer attribution. Two large contrasting text panels at the bottom (one dark, one accent2-color) with thematic icons.

**Section type B — "Album" (cream nostalgia paper):**
Cream paper background with a subtle dotted micro-pattern (masked at edges). Optional giant faded handwritten word in accent2 color at very low opacity. Headline panel: pure-white rounded card with shadow. Beside it, a quote card: dark background, accent-colored quote icon, font-accent (handwritten) testimonial, attribution underline. Body: polaroid bento grid — one large featured polaroid (`md:col-span-2 md:row-span-2`, -1.5° rotation) containing the PRODUCT_IMAGE inside a gradient frame with motif corner-tucks and a tag badge, plus 4 smaller polaroids each with a thematic icon-on-gradient image area, all with yellow tape, all with handwritten captions, slight different rotations.

**Section type C — "Roast" (dark contemplation):**
Dark background with radial accent and accent2 glows in opposite corners, plus the masked grid texture. Floating motif SVGs at very low opacity. Headline panel: `liquid-glass-strong` rounded panel with the accent-glow heading inside. Side label: `glass-pill` with a thematic icon and a one-line phrase. Body: **three pricing cards with three different visual treatments** (this variety is essential — do not make three identical cards):
  1. Cream paper card with red/accent border, peanut-brown dark text, dashed-stamp badge top-right, classic 5.90 numeral, dark CTA.
  2. **Highlighted card** — accent-color gradient background, slightly larger (negative margin top to lift), ribbon at top-right, accent2 huge price numeral, accent2 CTA with intense glow.
  3. Dark card with accent2 trim, accent2 numeral with glow, motif icon, cta-primary button.

**Section type D — "Signal" (the final action):**
Full-bleed strong accent color (often red/orange/green) with two large blurred orbs of accent2 in opposite corners and a giant centered accent2 oval blur behind the text. Floating motif SVGs at 30% opacity. A single contained panel (dark-translucent `liquid-glass` style with the accent color tint) holding: stamp badge eyebrow at -2°, MASSIVE headline (60→148px responsive) mixing display-black and a handwritten line in the middle, ending with a short final word. Subtitle below in 2 lines. Big primary CTA button (cream background, accent text) with a small dot indicator pulsing. Optional secondary outlined link. Logo flanked by horizontal dividers ("מאת <BRAND> / by <BRAND>") at the bottom.

**Section type E — "Workshop" / "Specs" (technical):**
For tech/SaaS products where one of the beats is "how it works". Dark background, alternating left/right two-column rows: a numbered eyebrow + heading + body on one side, a glass card with code/diagram/screenshot on the other. Strong vertical rhythm. Use this in place of B or C if BRAND_CONTEXT is technical.

Pick 4 from the library matching the narrative arc, in the order that feels right. Always end with type D (Signal) so the final beat is action.

---

### PHASE 8 — Hard rules (priority over any contradicting "best practice")

1. **No background on the outer wrapper `<div>`.** Only `body` gets `bg-background`. Anything else hides the video.
2. **Hero video is `position: fixed; -z-index: 20`** — it lives across the full document but is covered by every opaque section below it. Re-encode with `-g 1 -keyint_min 1`.
3. **Each non-hero section is fully opaque** with its own background class. Never use a partial scrim to "let the hero peek through" all sections — that's monotony pretending to be art.
4. **Each section has its own visual identity.** Different background, different palette emphasis, different layout pattern. Five sections must not look like five variations of one card grid.
5. **The narrative arc drives the section order.** Start with the emotion the BRAND_CONTEXT establishes; end with action. Don't pick sections at random.
6. **Headlines stay readable on busy backgrounds.** Every floating text block (heading, quote, subtitle, cursor cue, badge) is wrapped in a panel — `liquid-glass-strong` over dark sections, white/cream card over light sections, `glass-pill` for small cues. No text floats naked over busy textures.
7. **Headline max sizes**: hero headline caps at 78px desktop so the product/subject in the video stays visible. Section headlines can reach 108px. Final CTA headline can reach 148px because nothing else competes there.
8. **Palette cohesion**: warm brand → no cool tones except the tiniest accent. Cool brand → no warm tones except the tiniest accent. Never use `#FFFFFF` for text — always use the project's `cream` value.
9. **Logo treatment**: use the logo file as-is. Don't invert, don't tint, don't crop, don't wrap in a colored box that competes. Sizing: nav h-9 / hero attribution h-12 / final-CTA attribution h-16 / mini-footer h-6.
10. **Real product photography wins over generated gradients.** If PRODUCT_IMAGE_FILE was provided, use it prominently — in the featured polaroid, as a hero-section side accent, or as the centerpiece of one of the pricing cards.
11. **Navbar is clickable and scroll-spy-able.** Each item has `{ label, target }`. Smooth-scroll to the section. `scroll-margin-top: 90px` on `section[id]` so they don't land under the nav.
12. **Scroll-to-top button** appears after 60% viewport scroll, fixed bottom-left in RTL / bottom-right in LTR, with a short language-appropriate label.
13. **RTL layout details**: hero text panel bottom-RIGHT not bottom-LEFT. Forward arrows = `ArrowLeft`. Cursor cue at bottom-LEFT. Mobile menu items right-aligned.
14. **LTR layout details**: hero text panel bottom-LEFT. Forward arrows = `ArrowRight`. Cursor cue at bottom-RIGHT.
15. **Favicon is the logo**, set in `index.html` via `<link rel="icon" type="image/svg+xml" href="/logo.svg" />`. Add `apple-touch-icon` too.
16. **Decorative motif SVGs** — design ONE in-file React component themed to BRAND_CONTEXT (peanut for food, paw for animals, circuit for tech, leaf for nature, bolt for energy, droplet for beverage). Use it as floating background decoration at low opacity, rotated at varied angles, in 3–6 instances per dark/bright section.
17. **Ghost typography**: at least one section should have a giant low-opacity (4–8%) word or number in a corner as background texture — the brand's founding year, a one-word emotion, the product's name. Big enough to read (200–300px) but faint enough to feel like a watermark.
18. **Handwritten accent**: use the script font for the section eyebrow (e.g. "המתכון" / "the recipe") at -2° rotation in the accent color above each section headline. Adds warmth. Also use it for the middle line of the final CTA headline to break the rhythm.
19. **Stamp badges** instead of plain pill labels for "established X" / "since YYYY" / "original" / "limited". Dashed border, uppercase, letterspaced.
20. **Highlight-circle** the single most important word in each section headline. Hand-drawn-feeling red oval. Only ONE per heading.
21. **Pricing cards must look different from each other.** Light / highlighted-accent / dark — three distinct visual treatments. The highlighted one is bigger, has a ribbon, glows.
22. **Polaroid pattern** for nostalgic memory cards: white card, yellow/accent tape, slight rotation per card, handwritten caption, gradient image area, hover-un-rotates to 0° and lifts.
23. **CTAs use the brand CTA gradient + glow** (`cta-primary` class). Always with an arrow icon. Always with a tiny pulsing dot indicator if it's the "primary primary" action.
24. **Run `npx tsc --noEmit` after writing.** It must pass with zero output. Then `npm run dev` and verify the server starts cleanly. Don't claim done until both pass.
25. **Don't add features the user didn't ask for** — no contact form, no email signup, no analytics, no cookie banner, no language switcher, no dark mode toggle. Ship the spec.
26. **All copy is in LANGUAGE.** No mixing English boilerplate into a Hebrew page or vice versa. The only allowed non-LANGUAGE text is the brand mark itself, font family names in CSS, and TypeScript/React identifiers.
27. **No emojis in code or copy** unless the brand voice demands them.
28. **No comments in code** unless explaining a non-obvious WHY (e.g. the isSeeking guard).

---

### PHASE 9 — Run and verify

1. `npx tsc --noEmit` → zero output.
2. `npm run dev` → Vite reports `ready in <ms>` with no errors.
3. Open the local URL.
4. **Hero check** — page loads, hero is visible, moving the mouse scrubs the video smoothly with no stutter. If the subject in the video moves right when the mouse moves left (or vice versa) and that feels wrong, ask the user before flipping the formula to `1 - (e.clientX / window.innerWidth)`.
5. **Section identity check** — scrolling past the hero reveals 4 sections each with its OWN opaque background, none of which is the hero video bleeding through. If any later section shows the baby/hero video underneath, the outer wrapper has a bg class — find and remove it.
6. **Navbar click test** — click each nav item, smooth-scroll lands on the right section under the nav (not covered by it). CTA button in nav scrolls to the final action section.
7. **Scroll-to-top test** — scroll past 60% viewport, the floating button appears bottom-left/right (per direction). Click → smooth scroll to top, button fades out.
8. **Logo check** — favicon visible in tab, logo at correct sizes in nav / hero / final / mini-footer, no inverts or tints applied.
9. **Asset check** — if a product image was provided, it appears at least once at significant size (featured polaroid or hero side accent), not just as a tiny thumbnail.
10. **Responsive sanity** — at 360px, 768px, 1280px widths, no horizontal scroll, no text overlap, the nav collapses to hamburger below md.
11. **Reduced motion** — set `prefers-reduced-motion: reduce` in devtools and reload. Scroll reveal should snap (no animation), smooth scroll should be instant.
12. If any check fails, **fix it before reporting done**. Do not leave it for the user.

Report the URL it printed and what palette + arc you chose.

---

## PROMPT END

---

## What this prompt encodes (notes for the human, not Claude)

This template bakes in every painful lesson from the Bamba build:

- **The all-keyframes ffmpeg flag** is the difference between premium and amateur. Standard video stutters during scrub because seeks snap to the nearest keyframe ~250 frames away.
- **The z-index trap on the outer wrapper** burned ~10 minutes the first time. Documented as the #1 hard rule so it never repeats.
- **The original mistake of using a partial scrim to bleed the hero through all sections** produced a horrific, monotonous result. The corrected approach — each section fully opaque with its own brand identity — is now PHASE 7 + hard rule #3. Any future model is forced into the better pattern.
- **The narrative arc** is what separates a portfolio page from a story. Bamba's arc was *longing → joy → nostalgia → contemplation → action*. The prompt forces you (or Claude) to articulate the arc up front so it actually drives the section choices.
- **The decorative motif system** (peanut SVGs for Bamba, paws for animals, circuits for tech) gives each project its own character without requiring custom illustrations.
- **Typography trinity per language** prevents the "default to Helvetica" failure mode. Hebrew gets Rubik/Assistant/Suez One. English gets Anton/Inter/Caveat. Etc.
- **Polaroid, stamp, ribbon, highlight-circle, ghost-text** — six reusable visual primitives that compose into "warm/editorial/premium" without ever feeling corporate.
- **No backgrounds-on-floating-text** rule fixes the readability issue that surfaced when the original yellow section had headings sitting naked on top of the yellow.
- **Hard rule #25 (don't add features)** prevents scope creep into contact forms / signup modals / cookie banners that the user didn't ask for.

Keep this file with each new project's working directory and update the YAML block at the top. Then paste the prompt and let Claude execute.
