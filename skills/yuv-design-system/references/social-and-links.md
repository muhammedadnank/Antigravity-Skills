# Bio, credentials & links — canonical reference

Yuval's full set of credentials, public handles, and URLs, plus drop-in HTML/JSX patterns for footers, profile cards, speaker bios, and "find me elsewhere" sections.

**Auto-include rule:** Whenever an output has a footer, contact section, profile block, credits panel, video end-screen, speaker bio, course page, or any "find me elsewhere" surface, include this set without asking. Don't request URLs — they're below.

---

## Credentials (canonical list — use in any bio surface)

| Credential | Phrasing variants |
|---|---|
| 2× GitHub Star | "2× GitHub Star", "two-time GitHub Star", "GitHub Star (twice)" |
| AWS Gen AI Superstar | "AWS Gen AI Superstar", "AWS GenAI Superstar" |
| AI commentator on Channel 12 News (Israel) | EN: "AI commentator on Channel 12 News", "Resident AI commentator on Channel 12 News (Israel)", "The AI guy on Channel 12 News" · HE: "מגיש פינת AI בחדשות 12" |
| AI Builder & Speaker | "AI Builder & Speaker", "AI Builder and Speaker", "Builder · Speaker · AI" |
| Technical Content Creator | "Technical Content Creator", "AI Educator", "Hebrew AI Educator" |
| Founder of YUV.AI | "Founder of YUV.AI", "Founder, YUV.AI" |
| Active communities across socials | "Active communities across X, Instagram, TikTok, YouTube, LinkedIn, Facebook, GitHub" |

### Drop-in one-liner bios

**Long (about page / course landing):**
> Yuval Avidani is a 2× GitHub Star, AWS Gen AI Superstar, and the resident AI commentator on Channel 12 News (Israel). Founder of YUV.AI, AI Builder & Speaker, and technical content creator with active communities across every major social platform. Builds, teaches, and ships AI that actually works.

**Medium (speaker intro / podcast guest blurb):**
> AI Builder & Speaker · 2× GitHub Star · AWS Gen AI Superstar · AI commentator on Channel 12 News · Founder of YUV.AI.

**Short (Twitter bio / video lower-third / 280-char):**
> 2× GitHub Star · AWS Gen AI Superstar · The AI guy on @news12israel · Founder @yuv_ai

**Hebrew (long):**
> יובל אבידני — מגיש פינת ה-AI בחדשות 12, GitHub Star פעמיים, AWS Gen AI Superstar, מייסד YUV.AI. בונה, מלמד, ומשגר AI שעובד. קהילות פעילות בכל הרשתות החברתיות.

**Hebrew (short):**
> מגיש פינת AI בחדשות 12 · GitHub Star כפול · AWS Gen AI Superstar · מייסד YUV.AI

### Credential badges block (visual surfaces)

For about sections, speaker pages, podcast art — render the credentials as a row of mono-font chips:

```html
<div class="credentials" style="display:flex;flex-wrap:wrap;gap:10px;margin:24px 0;font-family:'JetBrains Mono',monospace">
  <span style="background:#FFEC00;color:#000;padding:6px 14px;font-size:11px;letter-spacing:0.2em;font-weight:700">2× GITHUB STAR</span>
  <span style="background:#5E17EB;color:#fff;padding:6px 14px;font-size:11px;letter-spacing:0.2em;font-weight:700">AWS GEN AI SUPERSTAR</span>
  <span style="border:1px solid #000;color:#000;padding:6px 14px;font-size:11px;letter-spacing:0.2em;font-weight:700">CHANNEL 12 · AI COMMENTATOR</span>
  <span style="border:1px solid #000;color:#000;padding:6px 14px;font-size:11px;letter-spacing:0.2em;font-weight:700">FOUNDER · YUV.AI</span>
</div>
```

---

---

## Machine-readable link set

```json
{
  "primary": {
    "website":  "https://yuv.ai",
    "linktree": "https://linktr.ee/yuvai"
  },
  "social": [
    { "id": "x",         "handle": "@yuvalav",         "url": "https://x.com/yuvalav",                       "label": "X",         "icon": "ph-x-logo" },
    { "id": "instagram", "handle": "@yuval_770",       "url": "https://instagram.com/yuval_770",            "label": "Instagram", "icon": "ph-instagram-logo" },
    { "id": "tiktok",    "handle": "@yuval.ai",        "url": "https://www.tiktok.com/@yuval.ai",           "label": "TikTok",    "icon": "ph-tiktok-logo" },
    { "id": "youtube",   "handle": "@yuv-ai",          "url": "https://youtube.com/@yuv-ai",                "label": "YouTube",   "icon": "ph-youtube-logo" },
    { "id": "github",    "handle": "@hoodini",         "url": "https://github.com/hoodini",                 "label": "GitHub",    "icon": "ph-github-logo" },
    { "id": "facebook",  "handle": "@yuval.avidani",   "url": "https://facebook.com/yuval.avidani",         "label": "Facebook",  "icon": "ph-facebook-logo" },
    { "id": "linkedin",  "handle": "yuval-avidani",    "url": "https://www.linkedin.com/in/yuval-avidani-87081474/", "label": "LinkedIn", "icon": "ph-linkedin-logo" }
  ]
}
```

For most use, just inline these URLs. For programmatic generation (e.g. building a Linktree-style page from data), use the JSON above.

---

## Surface-by-surface inclusion rules

| Surface | What to include |
|---|---|
| Full website footer | All 7 socials + website + linktree, as icon-only buttons in the brand color. Order: X · Instagram · TikTok · YouTube · GitHub · Facebook · LinkedIn · Linktree · Website. |
| Speaker bio / about card | Website + LinkedIn + Linktree + one signature social (X for technical audience, Instagram for general). |
| Video end-screen | Website + 3 socials (X · Instagram · YouTube). |
| Email signature / certificate footer | Website + LinkedIn + Linktree. Plain text or compact icons. |
| Slide deck closing slide | Linktree-as-shortcut (single QR or single URL). Don't list all 8 on a slide — too noisy. |
| Social card "find me elsewhere" graphic | Same as full website footer order. |
| LinkedIn post / Twitter bio CTA | Linktree URL — one tap, everything. |

---

## Drop-in HTML — Fly High mode

```html
<footer class="yuv-socials" style="
  display:flex; gap:18px; align-items:center; justify-content:center;
  padding:48px 0; background:var(--yuv-grey); font-family:'Inter',sans-serif;
">
  <a href="https://yuv.ai" aria-label="Website" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-globe"></i></a>
  <a href="https://x.com/yuvalav" aria-label="X" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-x-logo"></i></a>
  <a href="https://instagram.com/yuval_770" aria-label="Instagram" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-instagram-logo"></i></a>
  <a href="https://www.tiktok.com/@yuval.ai" aria-label="TikTok" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-tiktok-logo"></i></a>
  <a href="https://youtube.com/@yuv-ai" aria-label="YouTube" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-youtube-logo"></i></a>
  <a href="https://github.com/hoodini" aria-label="GitHub" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-github-logo"></i></a>
  <a href="https://facebook.com/yuval.avidani" aria-label="Facebook" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-facebook-logo"></i></a>
  <a href="https://www.linkedin.com/in/yuval-avidani-87081474/" aria-label="LinkedIn" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-linkedin-logo"></i></a>
  <a href="https://linktr.ee/yuvai" aria-label="Linktree" style="color:#5E17EB;font-size:22px;text-decoration:none"><i class="ph ph-tree-structure"></i></a>
</footer>
<!-- Phosphor icons: <script src="https://unpkg.com/@phosphor-icons/web"></script> -->
```

For Warm Editorial mode, swap `color:#5E17EB` → `color:#FF1464` and `background:var(--yuv-grey)` → `background:var(--off-white)`.

## Drop-in JSX — React + Phosphor

```tsx
const SOCIALS = [
  { url: 'https://yuv.ai',                                              label: 'Website',   Icon: Globe },
  { url: 'https://x.com/yuvalav',                                       label: 'X',         Icon: XLogo },
  { url: 'https://instagram.com/yuval_770',                             label: 'Instagram', Icon: InstagramLogo },
  { url: 'https://www.tiktok.com/@yuval.ai',                            label: 'TikTok',    Icon: TiktokLogo },
  { url: 'https://youtube.com/@yuv-ai',                                 label: 'YouTube',   Icon: YoutubeLogo },
  { url: 'https://github.com/hoodini',                                  label: 'GitHub',    Icon: GithubLogo },
  { url: 'https://facebook.com/yuval.avidani',                          label: 'Facebook',  Icon: FacebookLogo },
  { url: 'https://www.linkedin.com/in/yuval-avidani-87081474/',         label: 'LinkedIn',  Icon: LinkedinLogo },
  { url: 'https://linktr.ee/yuvai',                                     label: 'Linktree',  Icon: TreeStructure },
];

export function SocialsFooter() {
  return (
    <footer className="flex items-center justify-center gap-5 py-12 bg-grey font-body">
      {SOCIALS.map(({ url, label, Icon }) => (
        <a key={url} href={url} aria-label={label} className="text-purple text-xl no-underline">
          <Icon weight="regular" />
        </a>
      ))}
    </footer>
  );
}
```

---

## "Meet your instructor" / speaker bio block (Fly High)

```html
<section class="bio" style="display:grid;grid-template-columns:280px 1fr;gap:48px;align-items:center;padding:80px 100px;background:var(--yuv-grey)">
  <img src="/assets/profile-yuval-studio.png" alt="Yuval Avidani"
       style="width:280px;height:280px;object-fit:cover;border:8px solid var(--yuv-purple);border-radius:0">
  <div>
    <span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.3em;color:var(--yuv-purple);font-weight:700">YOUR INSTRUCTOR</span>
    <h2 style="font-family:'Anton',sans-serif;font-size:88px;line-height:1;letter-spacing:0;text-transform:uppercase;margin:12px 0 16px">Yuval Avidani</h2>
    <p style="font-family:'Inter',sans-serif;font-size:18px;line-height:1.5;color:#000;max-width:60ch">
      Founder of YUV.AI — Israel's leading Hebrew AI educator and technical innovator.
      Builds, teaches, and ships AI that actually works.
    </p>
    <div style="margin-top:24px;display:flex;gap:14px">
      <a href="https://yuv.ai" style="font-family:'Anton',sans-serif;text-transform:uppercase;padding:12px 24px;background:var(--yuv-purple);color:#fff;text-decoration:none;border-radius:999px;letter-spacing:0.04em">yuv.ai</a>
      <a href="https://linktr.ee/yuvai" style="font-family:'Anton',sans-serif;text-transform:uppercase;padding:12px 24px;border:2px solid var(--yuv-black);color:var(--yuv-black);text-decoration:none;border-radius:999px;letter-spacing:0.04em">linktree</a>
    </div>
  </div>
</section>
```

---

## Linktree-as-shortcut pattern

For closing slides, QR-code-friendly surfaces, and "where to follow next" CTAs, default to **a single linktree URL** instead of listing all 8 platforms. One link, one tap, everything. Pair with a QR rendered from the URL for live keynotes.

```html
<a href="https://linktr.ee/yuvai" style="font-family:'Anton',sans-serif;font-size:48px;text-transform:uppercase;color:var(--yuv-purple);text-decoration:none;letter-spacing:0">
  linktr.ee/yuvai
</a>
```

---

## Domain / handle inventory (for copy-paste)

- **Email:** `info@yuv.ai`
- **Brand name:** YUV.AI / yuv.ai
- **Tagline:** *Let's Fly High* (also the wordmark on `logo-rectangle-wordmark.png`)
- **Primary handle:** `@yuvalav` (X), `@hoodini` (GitHub)
- **Brand handle variants:** `@yuval_770` (IG), `@yuval.ai` (TikTok), `@yuv-ai` (YouTube), `@yuval.avidani` (FB)
- **One-link shortcut:** https://linktr.ee/yuvai
