"""Generate transcript_review.txt — the human-editable transcript.

Reads transcript.json (word-level whisper output) and emits a flat text file
that the user can edit. Each line is one whisper segment with a [mm:ss] prefix.

Usage:
    python make_review.py [path/to/transcript.json]

If a `corrections.json` exists in the same directory, it's applied first
(format: {"wrong": "right", ...} keyed on stripped tokens).
"""

import json, os, re, sys


def fmt_time(t):
    m, s = divmod(int(t), 60)
    return f"{m:02d}:{s:02d}.{int((t - int(t)) * 100):02d}"


def load_corrections(transcript_path):
    cdir = os.path.dirname(os.path.abspath(transcript_path)) or "."
    cpath = os.path.join(cdir, "corrections.json")
    if os.path.exists(cpath):
        with open(cpath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def correct(token, table):
    """Correct a token while preserving leading space and trailing punctuation."""
    lead = ""
    if token.startswith(" "):
        lead = " "
        token = token[1:]
    m = re.match(r"^(\S+?)([.,!?;:]*)$", token)
    core, tail = (m.group(1), m.group(2)) if m else (token, "")
    if core in table:
        core = table[core]
    return lead + core + tail


def main():
    tpath = sys.argv[1] if len(sys.argv) > 1 else "transcript.json"
    out_path = os.path.join(os.path.dirname(os.path.abspath(tpath)) or ".", "transcript_review.txt")

    with open(tpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    corrections = load_corrections(tpath)
    applied = {}

    # Apply corrections to every word and rebuild segment text.
    for seg in data:
        new_words = []
        for w in seg["words"]:
            original = w["word"]
            corrected = correct(original, corrections)
            if corrected.strip() != original.strip() and original.strip() in corrections:
                k = original.strip()
                applied[k] = applied.get(k, 0) + 1
            new_words.append({**w, "word": corrected})
        seg["words"] = new_words
        seg["text"] = "".join(w["word"] for w in new_words).strip()

    # Persist the corrected baseline back to transcript.json (so apply_review.py
    # can diff against the same starting state the user saw).
    with open(tpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    # Emit the review file.
    lines = []
    lines.append("# Transcript Review")
    lines.append("# Edit the TEXT of any line — fix mishears, tighten phrasing.")
    lines.append("# KEEP the [mm:ss.xx] prefix unchanged — that anchors the word timings.")
    lines.append("# Save the file and tell the agent to continue.")
    lines.append("")
    for seg in data:
        lines.append(f"[{fmt_time(seg['start'])}] {seg['text']}")
    lines.append("")
    lines.append("# === CORRECTIONS APPLIED ===")
    if applied:
        for k, n in sorted(applied.items(), key=lambda kv: -kv[1]):
            lines.append(f"# {k} → {corrections[k]} (×{n})")
    else:
        lines.append("# (no corrections needed)")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"wrote {out_path}")
    print(f"{len(data)} segments, {sum(len(s['words']) for s in data)} words")


if __name__ == "__main__":
    main()
