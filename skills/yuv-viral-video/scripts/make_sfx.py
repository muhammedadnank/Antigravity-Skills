"""Generate SFX with ElevenLabs sound-generation."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import requests

EDIT = Path(r"C:\Users\User\Desktop\edit")
SFX = EDIT / "sfx"
SFX.mkdir(parents=True, exist_ok=True)

KEY = None
for line in (Path.home() / "Developer/video-use/.env").read_text().splitlines():
    if line.startswith("ELEVENLABS_API_KEY="):
        KEY = line.split("=", 1)[1].strip()

URL = "https://api.elevenlabs.io/v1/sound-generation"

PROMPTS = [
    ("whoosh.mp3",   "fast tight whoosh transition swoosh, 350ms, sharp",                           0.5),
    ("impact.mp3",   "deep boom impact thud, sub-bass slam, single hit, no tail",                    0.7),
    ("riser.mp3",    "short rising synth riser build into impact, 1 second, energetic",              1.2),
    ("ding.mp3",     "high-pitched bright ding notification chime, single hit, 250ms",               0.5),
    ("typing.mp3",   "fast mechanical keyboard typing burst, multiple keystrokes, 1.2 seconds",      1.4),
    ("glitch.mp3",   "short digital glitch transition sound, 400ms, sharp tech",                     0.5),
    ("bass_drop.mp3","bass drop sub-bass thump, deep punchy, single hit no tail",                    0.7),
]

for name, prompt, dur in PROMPTS:
    out = SFX / name
    if out.exists():
        print(f"  cached: {name}")
        continue
    print(f"  generating {name} ({dur}s) ...", flush=True)
    r = requests.post(URL, headers={"xi-api-key": KEY, "Content-Type": "application/json"},
                      json={"text": prompt, "duration_seconds": dur, "prompt_influence": 0.6}, timeout=120)
    if r.status_code != 200:
        print(f"    ERROR {r.status_code}: {r.text[:200]}")
        sys.exit(1)
    out.write_bytes(r.content)
    print(f"    saved {len(r.content)//1024} KB")

print("\nall SFX generated")
