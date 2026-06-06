# Warm Editorial — alternate palette mode

The pink / yellow / bone variant. Use only for projects in this brand family:

- **Hope** — the cheetah video series and related campaign content
- **Marcus** — the white lion content
- **bigcats.ai**
- **practical.yuv.ai** — the course landing page
- Anywhere a "warm, confrontational, paper-feel, editorial" mood fits better than the Fly High "bold, electric, optimistic" mood

For everything else — keynotes, dashboards, technical product pages, hackathon decks — default to Fly High.

---

## Tokens

```css
:root {
  --pink:       #FF1464;   /* primary brand, CTAs, thread color */
  --yellow:     #E5FF00;   /* accent — when it shows up, it dominates */
  --black:      #0A0A0A;   /* warm near-black, never blue-black */
  --off-white:  #FAFAF7;   /* paper-feel, replaces #FFFFFF entirely */
  --bone:       #F5EEE4;   /* transitional sections, cream */
  --charcoal:   #1A1A1A;   /* primary text on light */
  --warm-gray:  #8B8680;   /* secondary text on light */
  --light-gray: #A8A39D;   /* secondary text on dark */
}
```

---

## Strict rules

- **Pure white `#FFFFFF` is banned.** Use `--off-white` for every surface a white would normally occupy. Page background, cards, text on dark.
- **Pink is the thread.** Appears in: logo, primary CTA, section accents.
- **Yellow dominates when it appears.** Full background block, full-width divider, large pull-quote field. Never a timid swatch.
- **Gradients only pink → yellow**, only on small surfaces (buttons, text underlines, icon fills). Never a full-page gradient wash.
- **Warm-toned shadows** with pink/orange undertone:
  ```css
  box-shadow: 0 8px 32px rgba(255, 20, 100, 0.08);     /* card */
  box-shadow: 0 20px 60px rgba(255, 20, 100, 0.12);    /* card-hover */
  ```
  Never blue-black shadows.
- **No `<PurpleBar>`** — that's Fly High. In Warm Editorial, content sections lead with a small bone-colored eyebrow + Anton headline. No vertical bar.

---

## Grain / paper texture (signature)

1–2% opacity SVG noise on light backgrounds for paper feel:

```css
body { background-color: var(--off-white); position: relative; }
body::before {
  content: '';
  position: fixed; inset: 0; pointer-events: none; z-index: 1; opacity: 0.02;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

Lift opacity to `0.04` for more pronounced grain; drop to `0.01` for subtle. Never above `0.05` — that's a visual noise, not a paper feel.

---

## Tailwind preset

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        pink: '#FF1464', yellow: '#E5FF00', black: '#0A0A0A',
        'off-white': '#FAFAF7', bone: '#F5EEE4',
        charcoal: '#1A1A1A', 'warm-gray': '#8B8680', 'light-gray': '#A8A39D',
      },
      fontFamily: {
        display: ['Anton', 'Rubik', 'sans-serif'],
        body:    ['Inter', 'Assistant', 'sans-serif'],
      },
      boxShadow: {
        warm:    '0 8px 32px rgba(255, 20, 100, 0.08)',
        'warm-lg':'0 20px 60px rgba(255, 20, 100, 0.12)',
      },
      maxWidth: { content: '1440px' },
    },
  },
};
```

---

## Differences from Fly High at a glance

| Aspect | Fly High | Warm Editorial |
|---|---|---|
| Primary brand | `#5E17EB` purple | `#FF1464` pink |
| Page background | `#F1F2F2` grey | `#FAFAF7` off-white |
| Pure `#FFFFFF` | Allowed on cards only | **Banned everywhere** |
| Yellow | `#FFEC00` | `#E5FF00` |
| Shadows | Plain low-opacity black | Warm pink/orange undertone |
| Grain | None — flat grey | 1–2% opacity SVG noise |
| Cards | White bg + 1px border + 4px purple left border | Off-white bg + warm shadow, no left border |
| Vertical accent | `<PurpleBar>` mandatory | Not used |
| Two-background rule | Yes (act / content) | No — single off-white canvas + occasional yellow section |
| Diagonal decoration | Rotated purple-dark in corners of act slides | Not typically used |
