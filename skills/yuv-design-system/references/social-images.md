# Social images, posters & OG cards

Patterns for static visual assets shared on social, in DMs, or embedded as preview cards.

---

## Canvas sizes

| Surface | Canvas | Aspect |
|---|---|---|
| Instagram feed (single) | 1080 × 1350 | 4:5 portrait |
| Instagram square | 1080 × 1080 | 1:1 |
| Instagram story / Reels cover | 1080 × 1920 | 9:16 |
| X / Twitter image | 1600 × 900 | 16:9 |
| LinkedIn feed | 1200 × 1200 (or 1200 × 627) | 1:1 or ~1.91:1 |
| Facebook / OG card | 1200 × 630 | ~1.91:1 |
| YouTube thumbnail | 1280 × 720 | 16:9 |
| TikTok cover | 1080 × 1920 | 9:16 |
| Podcast art (squared) | 3000 × 3000 (export as 1400 min) | 1:1 |

Design at the maximum useful size and downsample for delivery. Anton holds up at any scale.

---

## The four basic layouts

### 1. Big stat card

For an announcement, milestone, or single-number flex. Brand watermark bottom-right. Linktree URL bottom-left.

- Background: grey (Fly High) or off-white (Warm Editorial).
- Big Anton stat at 240–360px, color `#000`. The `%` or unit in brand color.
- JetBrains Mono eyebrow above (tracking 0.3em), in brand color.
- Inter 500 caption below explaining what the number means.
- Brand watermark `logo-rectangle-wordmark.png` bottom-right at ~140px wide.

### 2. Headline-only social card

For a punchline, quote, or hot take. Watermark bottom-right.

- Background: brand color (purple in Fly High act mode, pink in Warm Editorial).
- 4–6 lines of Anton headline. One word highlighted with the yellow `box-decoration-break: clone` span pattern.
- Attribution in Inter 500, 16–22px, color `rgba(255,255,255,0.7)` (on purple) or `rgba(0,0,0,0.55)` (on grey).
- Watermark bottom-right.

### 3. "Find me elsewhere" card

For directing followers to other platforms. Use the canonical link set.

- Background: grey.
- `logo-square-color.png` top-center at ~360px.
- Anton "LET'S CONNECT" headline at ~96px.
- Row of social icons (Phosphor) at 48px each, in brand color, with handles in JetBrains Mono below each icon.
- Linktree URL at bottom in Anton, ~64px.
- Watermark bottom-right.

### 4. "About me" / speaker bio card

For LinkedIn / Twitter pinned post / speaker page.

- 50/50 split. Left: `profile-yuval-studio.png` cropped square, with 8px brand-color border, radius 0.
- Right: eyebrow ("YOUR HOST" / "FOUNDER · YUV.AI") in JetBrains Mono. Anton "Yuval Avidani" headline. Inter body with credentials (see `social-and-links.md` § Credentials). Pill CTA to website.

---

## Mandatory watermark

Every social image gets the brand watermark in the bottom-right corner.

- Source: `assets/logo-rectangle-wordmark.png`
- Width: 12–15% of the canvas width (e.g. 160–180px on a 1080-wide image).
- Margin: 3% of canvas from right and bottom (≈32px on a 1080 canvas).
- Opacity: 100% on light backgrounds, 90% on dark.
- Never stretch. Preserve aspect.

---

## Type sizes on social images (1080-wide canvas)

| Role | Size |
|---|---|
| Hero stat | 240–320px Anton |
| Headline | 88–140px Anton |
| Section eyebrow | 18–22px JetBrains Mono, tracking 0.3em |
| Body / supporting copy | 28–36px Inter 400 |
| Caption / footer | 20–24px Inter 500 |

---

## Image generation prompts (Nano Banana 2 / Veo)

When generating imagery for social cards, use the brand palette explicitly in the prompt. Examples:

- *"Hero shot of a phoenix taking off, electric purple and yellow palette, on a clean light-grey background, cinematic studio lighting, no text, square 1:1"* (for Fly High)
- *"Editorial portrait, warm pink and bone palette, paper-grain texture, asymmetric composition, no text, 4:5 portrait"* (for Warm Editorial)

Avoid generic "AI art" prompts — always specify the palette explicitly and "no text" (Nano Banana 2 + most diffusion models render text poorly).

---

## Self-check before posting a social image

1. Canvas size matches the target platform exactly.
2. Watermark is in the bottom-right at the correct size.
3. All type is in the system fonts (Anton / Inter / JetBrains Mono / Rubik / Assistant).
4. Palette is brand-only (no stray default colors).
5. If text-heavy: the headline answers "what is this?" in under 2 seconds.
6. If number-heavy: there's exactly one hero stat, sized to dominate.
7. No emoji on enterprise / business surfaces. Casual / personal posts can use 1–2 sparingly.
8. Linktree URL or website URL visible if the image is meant to drive traffic.
