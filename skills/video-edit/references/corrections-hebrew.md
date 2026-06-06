# Known Hebrew Whisper Mishears (`large-v3`)

Seed your generator's `CORRECTIONS` dict with these. Keys are the wrong token that
Whisper outputs; values are the correct Hebrew. Apply by exact-match on the stripped
token (preserving trailing punctuation).

```python
CORRECTIONS_HE = {
    # Claude (the AI) — comes out as "cloud" cognate
    "קלוט": "קלוד",
    "לקלוט": "לקלוד",
    "מקלוט": "מקלוד",

    # other product / loanwords
    "אישות": "שוט",          # cinematic SHOT
    "מודי": "דפי",           # landing PAGES (not "moods")
    "מהמדהים": "המהמם",       # "the stunning"
    "המאמם": "המהמם",
    "התירוף": "הטירוף",       # "the madness"
    "מהתחלס": "מהתחלה",       # from the start
    "החתונה": "תחתונה",       # שורה תחתונה — bottom line

    # subject names / pronouns gone wrong
    "הרגע": "האריה",         # context: Marcus THE LION

    # routine spelling slips
    "מזגיר": "מזכיר",
    "אשמחים": "אשמח",
    "ערב": "ערך",            # value (not evening)
}
```

## Notes

- `ערב` legitimately means "evening" — only auto-correct if the surrounding context is
  clearly about value (e.g. "אם קיבלתם ערך" at the end of a sign-off). If in doubt,
  leave it for the user to fix in the review step.
- `קלוט` and variants — Whisper consistently mishears Claude. Force-replace.
- Names of channels, animals, places (Hope, Marcus, Midbarium) — usually correct, but
  spot-check in review.
- For English-mixed Hebrew (the speaker says "Claude Code" in English mid-sentence),
  Whisper may transliterate awkwardly. Replace the transliteration with the English term
  in Latin letters: `קלוד קוד` → `Claude Code` for cleaner captions.

## How to add new corrections

When you spot a new repeated mishear during transcript review:
1. Add it to the project's `gen_body.py` CORRECTIONS dict (one-off).
2. If it's a generally useful correction (brand name, common Hebrew vocab) — also append
   it to this file so the next project starts with it.
