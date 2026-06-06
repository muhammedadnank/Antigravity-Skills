# Setup — yuv-viral-video

This skill builds on top of the **video-use** skill (cuts, transcription, motion). Install that first via `~/Developer/video-use/install.md`. The pieces below are the additional dependencies this skill needs on top of video-use.

## Prerequisites

| Tool | Why | Install |
|------|-----|---------|
| `ffmpeg` ≥ 4.x | Everything | `brew install ffmpeg` (macOS) / Windows: `winget install ffmpeg` / Linux: `apt install ffmpeg` |
| Python ≥ 3.10 with PIL/numpy/requests | Card rendering, ASS generation | `uv pip install pillow numpy requests` |
| `python-bidi` | Hebrew RTL reordering for PIL | `uv pip install python-bidi` |
| `fontTools` + `brotli` | Convert Rubik woff2 → ttf (needed once) | `uv pip install fonttools brotli` |
| ElevenLabs API key | Scribe transcription + sound generation | https://elevenlabs.io/app/settings/api-keys → write to `~/Developer/video-use/.env` |
| Anton + Rubik TTF | Fonts (English Anton, Hebrew Rubik) | Bundled in `assets/fonts/` |

## Bundled fonts

The skill ships these because download URLs change and CDN paths break:

```
assets/fonts/Anton-Regular.ttf   161 KB — Google Fonts Anton (display, English)
assets/fonts/Rubik-Black.ttf      13 KB — Rubik 900 weight (Hebrew + Latin merged)
assets/fonts/Rubik-Bold.ttf       13 KB — Rubik 700 weight (Hebrew + Latin merged)
```

If these get corrupted or you need to refresh them, re-fetch:

```bash
# Anton (full TTF directly from gstatic — old-UA trick)
curl -sL -H "User-Agent: Mozilla/5.0" \
  "https://fonts.gstatic.com/s/anton/v25/1Ptgg87LROyAm0K08i4gS7lu.ttf" \
  -o assets/fonts/Anton-Regular.ttf

# Rubik — only woff2 is served. Merge Latin + Hebrew subsets:
mkdir -p /tmp/rubik && cd /tmp/rubik
curl -sL "https://cdn.jsdelivr.net/npm/@fontsource/rubik/files/rubik-hebrew-900-normal.woff2" -o he.woff2
curl -sL "https://cdn.jsdelivr.net/npm/@fontsource/rubik/files/rubik-latin-900-normal.woff2" -o lat.woff2
python -c "
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
m = Merger()
font = m.merge(['lat.woff2', 'he.woff2'])
font.flavor = None
font.save('Rubik-Black.ttf')
"
cp Rubik-Black.ttf <skill>/assets/fonts/
# Repeat for 700/Bold
```

## ElevenLabs API key

Write to `~/Developer/video-use/.env`:

```
ELEVENLABS_API_KEY=sk_...
```

This skill reads from that file directly (via `make_sfx.py`) so the key only lives in one place across both skills.

Quick sanity check:
```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  -H "xi-api-key: $(sed -n 's/^ELEVENLABS_API_KEY=//p' ~/Developer/video-use/.env)" \
  https://api.elevenlabs.io/v1/user
# 200 = good, 401 = bad token
```

## One-time pre-render: layout assets

The dark-mode background and speaker masks are static — generate them once per project:

```bash
python scripts/make_layout_assets.py  # writes layout_assets/bg_*.png, speaker_mask_*.png
```

Re-run only if you change SPEAKER_9X16 / SPEAKER_16X9 dims in `apple_glass.py`.

## Per-project workflow

```bash
cd <videos_dir>/edit/
# 1. Transcribe (uses video-use skill)
python ~/Developer/video-use/helpers/transcribe.py <source.mp4> --edit-dir .
python ~/Developer/video-use/helpers/pack_transcripts.py --edit-dir .

# 2. Author edl.json (cuts, layout per range, motion per beat) by hand from the packed transcripts

# 3. Generate SFX (one-time per project)
python <skill>/scripts/make_sfx.py    # generates sfx/*.mp3 via ElevenLabs

# 4. Pick archetype:
#    Screen-share + speaker PIP corner → build_screen_share.py
#    Full-frame selfie speaker         → build_selfie.py
python <skill>/scripts/build_<archetype>.py

# 5. Render cards + anims
python <skill>/scripts/make_cards_<archetype>.py
python <skill>/scripts/make_anims.py     # only if METRICS / AUTO beats present

# 6. Karaoke
python <skill>/scripts/make_karaoke.py

# 7. Composite
python <skill>/scripts/composite_<archetype>.py
```

Each composite increments `OUT_VERSION` so finals are saved as `final_9x16_V<N>.mp4`. Bump `OUT_VERSION` before re-rendering to keep backups.

## Dependencies summary

```
# requirements.txt
pillow>=10
numpy>=1.24
requests>=2.30
python-bidi>=0.6
fonttools>=4.50
brotli>=1.1
librosa>=0.10        # only used by video-use, kept for completeness
matplotlib>=3.7      # ditto
```
