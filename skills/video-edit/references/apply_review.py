"""Apply the user's edited transcript_review.txt back into transcript.json.

Inline ``::style=<id>`` markers (written by the transcript-editor webapp's
style picker) are also parsed and mirrored into ``caption_styles.json`` so
``gen_body.py`` can pick them up.

Parses each `[mm:ss.xx] text` line, matches it to the corresponding segment in
transcript.json by start time, re-tokenises the new text, and redistributes the
original word timings to the new tokens by sequential position + character weight.

Usage:
    python apply_review.py [path/to/transcript_review.txt]

After this runs, re-run gen_body.py to regenerate captions and then render.
"""

import json, os, re, sys


def parse_time(s):
    parts = re.split(r"[:.]", s.strip())
    if len(parts) == 3:
        m, sec, hund = parts
        return int(m) * 60 + int(sec) + int(hund) / 100.0
    if len(parts) == 2:
        m, sec = parts
        return int(m) * 60 + float(sec)
    return float(s)


def redistribute_words(new_text, orig_words):
    """Distribute the timing span of orig_words to new tokens of new_text."""
    new_tokens = re.findall(r"\S+", new_text)
    if not new_tokens:
        return []
    if not orig_words:
        return [{"word": tok, "start": 0.0, "end": 0.0} for tok in new_tokens]

    total_start = orig_words[0]["start"]
    total_end = orig_words[-1]["end"]
    total_span = max(total_end - total_start, 0.01)

    # Weight by char count so longer tokens get proportionally more time.
    weights = [max(len(t), 1) for t in new_tokens]
    total_w = sum(weights)

    out = []
    t = total_start
    for tok, w in zip(new_tokens, weights):
        dur = total_span * w / total_w
        out.append(
            {"word": " " + tok if out else tok, "start": round(t, 3), "end": round(t + dur, 3)}
        )
        t += dur
    # Snap last word end exactly to the original end.
    if out:
        out[-1]["end"] = round(total_end, 3)
    return out


def main():
    rpath = sys.argv[1] if len(sys.argv) > 1 else "transcript_review.txt"
    proj_dir = os.path.dirname(os.path.abspath(rpath)) or "."
    tpath = os.path.join(proj_dir, "transcript.json")

    with open(rpath, "r", encoding="utf-8") as f:
        review = f.read()

    # Parse the [mm:ss.xx] text lines (ignore # comments + blanks).
    # Inline style markers may appear at end of line as `  ::style=<id>`.
    pattern = re.compile(r"^\[([0-9:.]+)\]\s*(.+?)\s*$")
    style_marker = re.compile(r"\s*::style=([a-z0-9_-]+)\s*$")
    edited = []
    for line in review.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        m = pattern.match(line)
        if not m:
            continue
        body = m.group(2)
        style = None
        sm = style_marker.search(body)
        if sm:
            style = sm.group(1)
            body = body[: sm.start()].rstrip()
        edited.append({"start": parse_time(m.group(1)), "text": body, "style": style})

    if not edited:
        print("ERROR: no [mm:ss.xx] lines found in review file", file=sys.stderr)
        sys.exit(1)

    with open(tpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Match edited lines to segments by closest start time.
    changes = 0
    style_count = 0
    inline_assignments = {}
    for ed in edited:
        # Find segment with closest start.
        best = min(data, key=lambda s: abs(s["start"] - ed["start"]))
        if abs(best["start"] - ed["start"]) > 1.0:
            print(f"WARN: no close match for [{ed['start']:.2f}] {ed['text'][:30]}...", file=sys.stderr)
            continue
        if best["text"].strip() != ed["text"].strip():
            changes += 1
        best["text"] = ed["text"]
        best["words"] = redistribute_words(ed["text"], best["words"])
        if ed["style"]:
            best["style"] = ed["style"]
            style_count += 1
            inline_assignments[str(data.index(best))] = {
                "start": best["start"],
                "style": ed["style"],
            }
        elif "style" in best:
            # User reset to auto by removing the marker
            del best["style"]

    with open(tpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    # If inline markers were used, mirror them into caption_styles.json so
    # gen_body.py only has to read one place. Don't clobber an existing sidecar
    # that already has more detail — merge instead.
    styles_path = os.path.join(proj_dir, "caption_styles.json")
    sidecar = {"version": 1, "assignments": {}}
    if os.path.exists(styles_path):
        try:
            with open(styles_path, "r", encoding="utf-8") as f:
                sidecar = json.load(f)
            if not isinstance(sidecar.get("assignments"), dict):
                sidecar["assignments"] = {}
        except Exception:
            sidecar = {"version": 1, "assignments": {}}
    sidecar["assignments"].update(inline_assignments)
    if inline_assignments or os.path.exists(styles_path):
        with open(styles_path, "w", encoding="utf-8") as f:
            json.dump(sidecar, f, ensure_ascii=False, indent=2)

    print(f"applied {changes} edits to {tpath}")
    if style_count:
        print(f"applied {style_count} caption-style override(s) -> caption_styles.json")
    print(f"{len(data)} segments, {sum(len(s['words']) for s in data)} words")
    print("\nNext: re-run gen_body.py and render.")


if __name__ == "__main__":
    main()
