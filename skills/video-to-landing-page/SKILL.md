---
name: video-to-landing-page
description: Turn any video into a cinematic scroll-driven landing page — Apple-style hero where scrolling progresses the visible frame through the video. Use when the user provides a video file and asks for "a landing page from this video", "scroll-frame website", "Apple-style scroll site", "hero that scrubs the video", "like the GitHub Copilot landing", or any equivalent. Extracts N evenly-spaced frames via ffmpeg, builds a self-contained HTML page with a sticky hero + JS scroll listener that swaps the visible frame as you scroll, plus headline, sections and CTA below. For YUV.AI projects, applies the yuv-design-system skill in Neon mode (pink/cyan/white, default for YUV.AI web) — Decks (purple/yellow) is reserved for slides only. For generic / non-YUV.AI projects, picks an appropriate palette per the source video. Output is one folder with `index.html` and a `frames/` directory — drop on any static host.
---

# Video → Scroll-Driven Landing Page

Build a cinematic landing page where the hero is a video playing **on scroll** instead of time — like Apple product pages or the GitHub Copilot landing. Frames are extracted from the source video and swapped as the user scrolls; below the sticky hero, normal-scroll sections carry copy and CTA.

## When to invoke

- User drops a video and asks for a **landing page**, **scrolling site**, **scroll-frame hero**, or **website from a video**
- Mentions of "Apple-style scroll", "GitHub Copilot landing", "scrub-on-scroll", "frame on scroll"
- Hebrew equivalents: "דף נחיתה מסרטון", "אתר עם גלילה", "סרטון בגלילה"

## Save location

**Default:** `~/Documents/yuv-projects/landings/<slug>/` — always save landing pages here so you can find them again. Create the parent directory if missing.

```bash
mkdir -p ~/Documents/yuv-projects/landings
cd ~/Documents/yuv-projects/landings
# Build <slug>/ here.
```

Final path: `~/Documents/yuv-projects/landings/<slug>/`. Tell the user where the landing lives at the end of every build.

---

## Workflow (8 steps)

1. **Probe the source** — `ffprobe` for duration, fps, dimensions, audio.
2. **Pick frame count** — default `80`. Floor `40` (choppy if lower), ceiling `160` (heavy page). Choose by duration: ≤10s → 50, 10–30s → 80, 30–60s → 120, >60s → 160.
3. **Decide output directory** — default `~/Documents/yuv-projects/landings/<slug>/`. The `<slug>` is short, derived from the video name or the topic. Override only on explicit request.
4. **Extract frames** — run `references/extract-frames.py <source-video> <output-dir> [count]`. Outputs `output-dir/frames/f_0001.jpg`… with consistent JPG quality 82 and a max-width of 1920 (downscaled if source is larger).
5. **Copy and customise** `references/landing-template.html` into `output-dir/index.html`:
   - Replace the `__FRAMES__` placeholder with `<img>` tags for each frame (the build script does this for you when you pass `--build-html`).
   - Fill in `__HEADLINE__`, `__TAGLINE__`, `__CTA_TEXT__`, `__CTA_HREF__`, sections.
   - For Hebrew content: set `<html lang="he" dir="rtl">` and swap fonts to Rubik/Assistant (see `references/design-notes.md`).
6. **Optimise frames** — the build script already scales to 1920px max-width. If the page total weight is > 12 MB, drop quality to 75 or reduce frame count.
7. **Preview** — `python -m http.server` inside the output directory and open `http://localhost:8000`. Scroll feels buttery on a decent machine.
8. **Deploy** — drop the folder on Vercel/Netlify/Cloudflare Pages. No build step needed.

## The scroll mechanic

- Outer scroller `.scroll-stage` height set in viewport units (default `600vh` = scroll 5 screens to traverse all frames).
- Sticky hero `position: sticky; top: 0; height: 100vh` containing all frames absolutely positioned and hidden except the active one.
- Scroll listener computes `progress = scrolledIntoStage / scrollableHeight` clamped 0–1.
- `idx = floor(progress * (N - 1))` — swap the `.active` class to that frame.
- Wrap the listener in `requestAnimationFrame` to keep 60fps.

## Design rules

- If the project is **YUV.AI-branded** (Yuval personally, his portfolio, his brand): call `yuv-design-system` and lock it to a mode by medium —
  - **Neon mode** (DEFAULT for YUV.AI web): hot pink (`#FF1464`) + neon cyan (`#00E5FF`) + white or rich black canvas. Anton + Inter (English) / Rubik + Assistant (Hebrew). 0px or 999px radii.
  - **Warm Editorial mode**: only for Hope, Marcus, bigcats.ai, practical.yuv.ai — pink + yellow + bone, off-white never pure `#fff`.
  - **Never use Decks mode (Fly High purple/yellow)** for a landing page — that palette is reserved for slide decks only.
- If the project is **not YUV.AI-branded**: do not apply yuv-design-system. Pick a palette that fits the source video's mood. Anton + Inter remain reasonable defaults but aren't mandatory.
- Hero overlays should be **subtle** — a vignette and a single big headline; don't drown the frame.
- Below-hero sections: light canvas (white in Neon mode, off-white in Warm Editorial, bone if going generic-warm), large Anton heading, body copy in Inter at 18–22px, CTA as a sharp pill (`border-radius: 999px`) — pink fill in Neon mode, brand-appropriate color otherwise.
- For Hebrew: respect RTL, use Rubik 900 for headlines, Assistant 400/500 for body.

## File references

| File | Purpose |
| --- | --- |
| `references/extract-frames.py` | ffmpeg-based frame extractor; optionally builds the full HTML in one go |
| `references/landing-template.html` | Self-contained landing-page skeleton with the scroll mechanic |
| `references/design-notes.md` | Typography, palette, and motion defaults |
