# Copy Guide — writing the five scenes

The animation is half the work. The copy is the other half. Generic copy will sink an otherwise beautiful landing. Read this before you write a single word of headline.

## The structural rule

Each of the 5 scenes is exactly three lines:

```
[KICKER]            ← 1–3 words, all caps, Anton, letter-spaced
[HEADLINE]          ← 2–4 words, broken across 2 lines with <br>
[HANDWRITTEN LINE]  ← 4–8 words, one full sentence, ends with a soft punctuation
```

The kicker frames the moment ("Chapter 02", "— A True Story —", "01 — Workflow"). The headline is the punch. The handwritten line is the emotional follow-through — the line that earns the trust the headline asked for.

Length matters because the typography is huge. A 6-word headline at 200px breaks the layout. Keep it tight.

## The five-beat arc

This structure is borrowed from short documentary editing — you have ~25 seconds of attention; spend each beat well.

| Scene | Beat | Job |
|---|---|---|
| 1 | **Hook** | Introduce the subject. Name it. State its essence in one phrase. |
| 2 | **Origin** | Where does it come from? What is its world? |
| 3 | **Stakes** | Why does it matter? Where does the story take place? |
| 4 | **Moment** | The personal turn — the speaker's act, the decision, the proximity. |
| 5 | **Resolution + CTA** | What happened. Then the call to action. |

You're not writing about a product. You're writing about a moment that includes a product.

## Voice rules

- **Anton headlines are commands or noun-phrases, never sentences.** "Born to Run." "Built for Flow." "Meet Marcus." Not "He was born to run." The handwritten line is where sentences live.
- **Handwritten lines are colloquial, almost spoken.** "the white lion of the Negev." "an AI that finally ships with you." "and knelt with food in my hands." Lowercase first word; trail off with a period (or `…` only for the loader script).
- **Avoid adjectives in the headline.** The image already shows the adjective. "Beautiful Cheetah" is wasted ink. "Born to Run" lets the image do the work.
- **Specifics beat abstractions.** "Be'er Sheva" beats "the desert". "macOS · Windows · Linux" beats "every platform". "70 mph" beats "fast".

## Three real examples — read these carefully

### GitHub Desktop (product)

```
SCENE 1
— A NEW CHAPTER —
GitHub
Desktop
the new build. native. fast. yours.

SCENE 2
01 — WORKFLOW
Where
Code Lives.
branches, PRs, reviews — at your fingertips.

SCENE 3
02 — PERFORMANCE
Built
For Flow.
native speed. zero friction. all platforms.

SCENE 4
03 — INTELLIGENCE
Copilot
Inside.
an AI that finally ships with you.

SCENE 5 (CTA)
— NOW AVAILABLE —
Ready?
macOS · Windows · Linux.
[ Download for macOS ] [ Windows ] [ Linux ] [ Next: Marcus → ]
```

### Marcus the white lion (personal moment, wildlife)

```
SCENE 1
— A TRUE STORY —
Meet
Marcus.
the white lion of the Negev.

SCENE 2
CHAPTER 01
Born
of the Desert.
a coat like snow over a land that burns.

SCENE 3
CHAPTER 02
Midbarium.
Be'er Sheva.
where wilderness meets wonder.

SCENE 4
CHAPTER 03
I Crossed
the Fence.
and knelt with food in my hands.

SCENE 5
— THE LAST FRAME —
And the
King Ate.
a moment frozen in time.
[ Visit Midbarium ] [ Open in Maps ] [ Next: Hope → ] [ ← Back ]
```

### Hope the cheetah (speed, motion, intimacy)

```
SCENE 1
— A TRUE STORY —
Meet
Hope.
the fastest heart in the Negev.

SCENE 2
CHAPTER 01
Born
to Run.
seventy miles an hour of wild grace.

SCENE 3
CHAPTER 02
Midbarium.
Be'er Sheva.
where the desert opens — she answers.

SCENE 4
CHAPTER 03
I Came
Close.
she looked at me — and let me stay.

SCENE 5
— THE LAST FRAME —
A Second
of Stillness.
with the fastest cat alive.
[ Visit Midbarium ] [ Open in Maps ] [ ← Back to showcase ]
```

## The accent color picks a tone

- `gold` (#f5b042) — warmth, reverence, mythic ("Marcus")
- `amber` (#ff8a3d) — heat, motion, vitality ("Hope")
- `accent` (pink #ff4d6d) — product/tech, modern, slightly playful ("GitHub")
- `cream` (#f5e9d4) — neutral, used inside scenes 2 and 4 for variety so every line isn't the same color

The convention in the references: scenes 1, 3, 5 use the page's signature accent; scenes 2 and 4 use `cream` for visual rhythm. Follow that unless you have a reason not to.

## Loader script tone

The loader sits on screen for about 1–3 seconds while frames preload. The handwritten line beneath the giant title should be a tiny hook — present-tense, ending in `…`.

Good examples (from the reference):
- `loading the new build…`
- `summoning the king of the Negev…`
- `summoning the runner…`

Bad: `Please wait while frames load.` (boring, breaks tone)

## Scroll hint tone

Short. Uppercase. 2–4 words. Often a verb tied to the subject:

- `SCROLL TO PLAY` (GitHub — software metaphor)
- `SCROLL TO ENTER` (Marcus — entering a kingdom)
- `SCROLL TO RUN` (Hope — running with the cheetah)

If you can't find a verb that suits the subject, fall back to `SCROLL TO BEGIN`.

## CTAs in the final scene

2–4 CTAs, the first one solid or accent-colored, the rest outlined. Keep them short — 2–4 words each. End with a chain link (`Next: X →`) if this is part of a showcase, and a back-to-hub link (`← Back to showcase`).

Available CTA classes:
- `cta` — outlined off-white (default)
- `cta solid` — filled off-white on bg
- `cta gold` — outlined gold (good for Midbarium / nature subjects)
- `cta amber` — outlined amber (Hope-style)

If introducing a new accent, add `.cta.<name>` rules to style.css in the same pattern as `.cta.gold`.
