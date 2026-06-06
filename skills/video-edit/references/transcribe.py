"""Hebrew transcription with TIGHT segmentation for accurate caption sync.

Default Whisper segments are 20-30s monolithic blocks — within them
word-level timestamps drift by 1-2s. We force shorter segments via:

  1. Silero VAD with min_silence_duration_ms=400 (default 2000) — splits
     at every natural pause.
  2. condition_on_previous_text=False — stops Whisper from concatenating
     short segments back into long ones.
  3. Post-process: any segment > 6s gets split at the nearest
     mid-segment word boundary using its own word timestamps.

CPU forced because local CUDA install lacks cuDNN.
"""

import json, sys
from faster_whisper import WhisperModel

m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=8)
segs, info = m.transcribe(
    "audio.wav",
    language="he",
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={
        "min_silence_duration_ms": 400,
        "speech_pad_ms": 200,
    },
    condition_on_previous_text=False,
)

print("language:", info.language, file=sys.stderr)

raw = []
for seg in segs:
    words = [
        {"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
        for w in (seg.words or [])
    ]
    raw.append(
        {
            "text": seg.text.strip(),
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "words": words,
        }
    )


# Post-process: split any segment > 6s into smaller pieces at the
# longest internal word-gap. Iterative until no segment exceeds the cap.
MAX_SEG = 6.0
out = []
queue = raw[:]
while queue:
    s = queue.pop(0)
    if s["end"] - s["start"] <= MAX_SEG or len(s["words"]) < 4:
        out.append(s)
        continue
    # Find the largest internal gap (silence between consecutive words).
    words = s["words"]
    best_i, best_gap = -1, 0.0
    for i in range(1, len(words) - 1):
        gap = words[i]["start"] - words[i - 1]["end"]
        # Bias toward the middle to avoid runt fragments.
        mid_bias = 1.0 - abs(i - len(words) / 2) / (len(words) / 2)
        score = gap * (0.6 + 0.4 * mid_bias)
        if score > best_gap:
            best_gap, best_i = score, i
    if best_i < 0:
        out.append(s)
        continue
    left_words = words[:best_i]
    right_words = words[best_i:]
    left = {
        "text": "".join(w["word"] for w in left_words).strip(),
        "start": left_words[0]["start"],
        "end": left_words[-1]["end"],
        "words": left_words,
    }
    right = {
        "text": "".join(w["word"] for w in right_words).strip(),
        "start": right_words[0]["start"],
        "end": right_words[-1]["end"],
        "words": right_words,
    }
    # Re-enqueue right side in case it also needs splitting
    queue.insert(0, right)
    out.append(left)

with open("transcript.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(
    f"{len(out)} segments (was {len(raw)} raw), "
    f"{sum(len(s['words']) for s in out)} words",
    file=sys.stderr,
)
print(
    f"Max segment length: {max(s['end']-s['start'] for s in out):.2f}s "
    f"(cap was {MAX_SEG}s)",
    file=sys.stderr,
)
