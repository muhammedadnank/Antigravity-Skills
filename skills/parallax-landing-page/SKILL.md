---
name: parallax-landing-page
description: Build a scroll-driven cinematic landing page from a short video. The user provides a 5–15 second video (often AI-generated); this skill extracts every frame at HD JPEG quality, then produces a single-hero HTML page where the user's scroll gesture scrubs the frames in place (the page itself never scrolls) and 5 dramatic text overlays crossfade in/out — Google Anton headlines, Caveat handwritten accents, locked body, virtual scroll. Use this skill whenever the user wants to "turn this video into a landing page", "make a scroll-scrub landing page", "build a parallax hero from this clip", "add a new landing page to the parasites showcase", "do the same as github/lion/hope for this new video", or any variant that pairs a short clip with dramatic scroll-triggered storytelling. Trigger even if the user only says "use my video for a landing page" — that is this skill.
---

# Parallax Landing Page

Turn a short video into a one-screen cinematic landing page where the user's scroll gesture scrubs through the video frame-by-frame while five dramatic text scenes crossfade in and out. The document never actually scrolls — wheel/touch/keyboard input is intercepted in JS and converted into virtual frame progress.

This skill encodes the patterns proven in the bundled reference at [`../../examples/parasites/`](../../examples/parasites/) (the github / lion / hope landings — three working pages built with this exact skill). Treat that folder as the ground truth if anything here is ambiguous.

## Where this skill sits in the YUV.AI pyramid

`parallax-landing-page` is in the **middle tier** of the YUV.AI skills pyramid, alongside `yuv-design-system`, `yuv-decks`, `yuv-viral-video`, and `video-to-landing-page`. The top-tier orchestrator `yuv-pilot` routes here whenever a 5–15s video clip needs to become a single-hero scroll-scrub landing.

This skill **brings its own visual language** (Anton + Caveat + Inter, gold/amber/accent/cream accent palette) — it does NOT call into `yuv-design-system`. The two systems coexist: yuv-design-system owns the brand palette across web/app/deck surfaces, parallax-landing-page owns the cinematic scroll-scrub aesthetic specifically. For YUV.AI parallax landings, you can OPTIONALLY add a phoenix watermark + the canonical Linktree URL in the footer area as a brand throughline — see `yuv-design-system/assets/` for the watermark file. Do NOT swap the Anton/Caveat type stack for the design system's Neon palette — that would lose the signature look.

## What you're building

Each landing is a single locked viewport with:
- A canvas filling the screen, drawing one frame at a time (cover-fit, DPR ≤ 2)
- 5 absolutely-positioned text scenes (kicker + uppercase Anton headline + Caveat handwritten line), each with its own scroll-progress window
- A fixed nav with `PARALLAX // showcase` logo and links to sibling landings
- A loader that preloads every frame before letting the user interact
- A vignette + film grain overlay
- A bottom scroll-hint that fades out once the user starts scrolling
- A bottom-right frame counter (e.g. `073 / 145`)
- A final scene that *is* the CTA section — no separate `.end` section below

Total weight at q:v 2: roughly 120–220 KB per frame × frame count. A 6-second 24fps clip = 145 frames ≈ 25 MB. A 10-second clip = 241 frames ≈ 53 MB.

## Save location

**Default:** `~/Documents/yuv-projects/landings/<slug>/` — always save standalone landings here so you can find them again. Override only if the user explicitly picks a different location OR if Mode B (integrate into the existing `examples/parasites/` showcase) is selected.

```bash
mkdir -p ~/Documents/yuv-projects/landings
cd ~/Documents/yuv-projects/landings
# The skill creates <slug>/ here as it extracts frames and builds the HTML.
```

Final path (Mode A — standalone): `~/Documents/yuv-projects/landings/<slug>/`.
Final path (Mode B — integrate): the existing showcase directory the user chose.

Tell the user the final path at the end of every build.

---

## Workflow

There are four phases. Don't skip phases — each one feeds the next.

### Phase 1 — Discover

Confirm with the user:
1. **Video path** — where the source MP4 lives.
2. **Slug** — short folder/file name (e.g. `hope`, `marcus`, `desk`). One word, lowercase, no spaces. This becomes both the frame folder name (`<slug>/`) and the HTML filename (`<slug>.html`).
3. **Theme / topic** — what is this landing about? A product launch? A personal moment? A wildlife encounter? You need this to write the copy.
4. **Project mode** — standalone (brand new folder) or integrate into the existing parasites showcase at `examples/parasites/` (top of this repo). If the user says "add it to the showcase", they mean Mode B below.
5. **Accent color** — for the script/CTA highlight: `gold` (#f5b042), `amber` (#ff8a3d), `accent` (pink #ff4d6d), `cream` (#f5e9d4), or something new (add it to `:root` in style.css and write a new `.script.<name>` rule).

If the user hasn't specified some of these, propose defaults and move on — don't stall on questions they can answer once they see the result.

### Phase 2 — Extract frames

Run the bundled extraction script. It probes the video with ffprobe and extracts every frame at native resolution with `-q:v 2` (near-lossless JPEG), naming them `frame-001.jpg` through `frame-NNN.jpg` (3-digit zero-padded).

```bash
python <skill>/scripts/extract_frames.py <video_path> <output_folder>
```

Example:
```bash
python C:/Users/User/.claude/skills/parallax-landing-page/scripts/extract_frames.py \
    C:/Users/User/Documents/parasites/hope/hope.mp4 \
    C:/Users/User/Documents/parasites/hope
```

The script prints a JSON metadata block to stdout. Capture it — you need `frame_count` and `suggested_scroll_budget` for the HTML.

Why `-q:v 2`: ezgif and similar tools re-compress aggressively (~55 KB/frame). Native ffmpeg at q:v 2 gives ~120–220 KB/frame at the same dimensions — visibly sharper. Do not downscale; never upscale (it inflates files without adding detail).

Why the scroll-budget formula (≈26 px per frame): keeps the tactile "pixels of scroll per frame advanced" constant across clip lengths. 145 frames → ~4200, 241 frames → ~6300, 90 frames → ~2500 (floor). The script computes it for you and clamps to `[2500, 8000]`.

### Phase 3 — Author the page

Read the template at `<skill>/assets/landing-page-template.html`. It is a complete working file with `{{PLACEHOLDER}}` markers and `<!-- TODO: -->` comments next to creative bits. Write a new file at `<target>/<slug>.html` with everything substituted.

Substitution checklist (every placeholder must be replaced):

| Placeholder | What to put | Example |
|---|---|---|
| `{{PAGE_TITLE}}` | HTML `<title>` | `Hope — The Fastest Heart in the Negev` |
| `{{PAGE_DESCRIPTION}}` | meta description, one sentence | `A moment with Hope, the cheetah of Midbarium.` |
| `{{SLUG}}` | folder name (no path, no slash) | `hope` |
| `{{FRAME_COUNT}}` | integer frame count | `241` |
| `{{FRAME_COUNTER_TEXT}}` | `001 / NNN` with matching width | `001 / 241` |
| `{{SCROLL_BUDGET}}` | integer from the extractor JSON | `6300` |
| `{{PREVIEW_FRAME_MID}}` | zero-padded middle frame | `121` |
| `{{PREVIEW_FRAME_END}}` | zero-padded last frame | `241` |
| `{{LOADER_TITLE}}` | one word, uppercase | `HOPE` |
| `{{LOADER_SCRIPT}}` | handwritten line ending in `…` | `summoning the runner…` |
| `{{NAV_LINKS_HTML}}` | full `<a>` tag block for nav | see below |
| `{{SCENE_N_*}}` | kicker, headline, handwritten line for each of 5 scenes | see copy guide |
| `{{SCROLL_HINT_TEXT}}` | 2–4 word uppercase prompt | `SCROLL TO RUN` |
| `{{CTA_BUTTONS_HTML}}` | 2–4 `<a class="cta">` tags | see below |
| `{{ACCENT_CLASS}}` | accent color suffix for `.script.X` and `.cta.X` | `amber` |

Read `references/copy-guide.md` for the cinematic copy patterns (kicker phrasing, headline length, handwritten line tone). The copy is where this skill earns its keep — generic copy will sink an otherwise beautiful animation.

### Phase 4 — Wire up assets

If the target folder already has `style.css` and `parallax.js` (showcase integration), do nothing — they're shared. Otherwise copy both from `<skill>/assets/` into the target folder:

```bash
cp <skill>/assets/style.css <target>/style.css
cp <skill>/assets/parallax.js <target>/parallax.js
```

If integrating into an existing showcase, also do the steps in `references/showcase-integration.md` — add a card to `index.html`, add a link to every existing landing's navbar, and add the chain CTA on the previous landing's final scene.

Tell the user how to view:
> Open `<target>/<slug>.html` via `python -m http.server 8000` from the parent folder (not `file://` — Chromium can taint the canvas with local image origins).

## File contract

```
<target>/
├── <slug>/                  # frame folder
│   ├── <slug>.mp4           # the source (preserved)
│   ├── frame-001.jpg
│   ├── frame-002.jpg
│   └── … frame-NNN.jpg
├── <slug>.html              # the landing page
├── style.css                # shared (copy if standalone)
├── parallax.js              # shared (copy if standalone)
└── index.html               # the hub (only if standalone or integration)
```

The frame folder name and the HTML filename MUST share the same slug — the `folder` option in the page's `new ParallaxPage({folder: '<slug>', ...})` call is the literal folder path.

## The ParallaxPage API (already in parallax.js, do not redefine)

```js
new ParallaxPage({
  folder:       '<slug>',     // folder containing frame-001.jpg, etc.
  frameCount:   145,          // integer
  prefix:       'frame-',     // always 'frame-' for this skill
  scrollBudget: 4200,         // pixels of accumulated input for full pass
  // optional: padWidth (default 3), ext (default 'jpg')
})
```

The class auto-attaches `body.scrub-page` (which locks scroll via CSS), preloads all frames, runs an RAF-driven lerp (0.22 factor) toward the scroll-derived target frame, and crossfades scenes whose `data-start`/`data-end` ranges include the current progress.

## Hard constraints (the non-negotiables)

These are baked into the reference and break the experience if violated:

- **5 scenes, fixed progress windows**: `0.00–0.20`, `0.22–0.40`, `0.42–0.60`, `0.62–0.80`, `0.82–1.00`. The 0.02 gap between scenes is intentional — it's a moment of "just the image, no text" between beats. The hero (scene 1) and final (scene 5) use `data-fade="0.30"` and `data-fade="0.18"` respectively so they hold longer at the edges; middle scenes use the default 0.25.
- **No `.end` section** beneath the scrub. The final scene contains the CTAs. The whole page is one locked viewport.
- **Anton + Caveat + Inter** — uppercase Anton for everything bold, Caveat for handwritten accents (gold/amber/cream), Inter for any body lead text. Never substitute, never add a fourth font.
- **Off-white `#f5f1ea`, never `#fff`** — already in CSS as `var(--text)`.
- **Frame names are `frame-NNN.jpg`** zero-padded to the width of the total (3 digits is the standard since clips < 1000 frames; the JS auto-computes counter width from the total).
- **The slug is the folder name AND the HTML filename basename** — `hope/`, `hope.html`. No exceptions; the integration steps assume this.

## Where to look when you get stuck

- The reference showcase bundled in this repo: [`examples/parasites/`](../../examples/parasites/) — github.html, lion.html, hope.html, style.css, parallax.js, index.html. If your output diverges visibly from those, you've drifted; reread.
- `references/copy-guide.md` — how to write the 5 scenes so they actually feel cinematic.
- `references/showcase-integration.md` — exact edits needed when adding to an existing hub.
- `assets/landing-page-template.html` — the canonical structure with placeholders.
- `assets/hub-template.html` — only used when creating a brand-new showcase (3 cards from scratch).

## Two real example invocations

**Standalone:** user has a single clip `desk.mp4` and wants a landing page.
1. Ask for slug + theme. Run extractor on `desk.mp4` → `./desk/frame-NNN.jpg`.
2. Copy `style.css` + `parallax.js` to project root.
3. Author `desk.html` from template. Nav has just one link: itself.
4. Done. Tell user to serve with `python -m http.server`.

**Showcase add:** user adds `hope.mp4` to the existing parasites folder.
1. Slug = `hope`. Extract → `hope/frame-NNN.jpg`. (Reuse existing style.css + parallax.js.)
2. Author `hope.html` from template.
3. Run showcase integration: add a third card to `index.html`, append a `Hope` link to the navbar in `github.html` and `lion.html`, chain the previous landing's final scene with a `Next: Hope →` CTA.
4. If introducing a new accent color, add it to `:root` and add `.script.X` + `.cta.X` rules in `style.css`.
