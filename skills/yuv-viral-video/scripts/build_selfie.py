"""V5 build for tt.mp4 — REVERTED to full-frame speaker (no PIP corner).
For tt.mp4 the speaker IS the content. Cards float on top in safe zones.
9:16 output: scale source 720x1280 -> 1080x1920 directly.
16:9 output: blurred zoomed source as background + crisp speaker centered.
Saves with _V5 suffix.
"""
from __future__ import annotations
import json, subprocess, time
from pathlib import Path

EDIT = Path(r"C:\Users\User\Downloads\tt_edit")
SRC = Path(r"C:\Users\User\Downloads\tt.mp4")
EDL = json.loads((EDIT / "edl.json").read_text(encoding="utf-8"))

SEG_V = EDIT / "segments_v5_9x16"
SEG_H = EDIT / "segments_v5_16x9"
SEG_V.mkdir(parents=True, exist_ok=True)
SEG_H.mkdir(parents=True, exist_ok=True)

VERSION = 5
BASE_V = EDIT / f"base_9x16_V{VERSION}.mp4"
BASE_H = EDIT / f"base_16x9_V{VERSION}.mp4"
GRADE = "eq=contrast=1.04:saturation=1.05:gamma=1.02"
FPS = 30

MOTION = {
    "HOOK":         ("snap_in",  0.06),
    "WORKSHOP":     ("dolly_l",  0.04),
    "STUDENT":      ("push_in",  0.05),
    "BUILD_15MIN":  ("snap_in",  0.05),
    "RESULT":       ("push_in",  0.04),
    "NO_PAY":       ("snap_in",  0.06),
    "MAGIC":        ("pull_out", 0.04),
    "CTA":          ("push_in",  0.05),
}


def motion_fragment(kind, amount, dur, w, h):
    if kind == "hold":
        return ""
    if kind == "push_in":
        zoom = f"(1 + {amount:.4f}*min(t/{dur:.4f},1))"
    elif kind == "pull_out":
        zoom = f"(1 + {amount:.4f}*max(1 - t/{dur:.4f},0))"
    elif kind == "snap_in":
        zoom = (f"(1.04 + {max(amount-0.04, 0):.4f}*"
                f"(1 - pow(1 - min(t/{dur:.4f},1), 3)))")
    elif kind == "dolly_l":
        zoom = f"(1 + {amount:.4f})"
    else:
        return ""
    if kind == "dolly_l":
        x_off = f"(-{0.05*amount*w:.2f}*t/{dur:.4f})"
    else:
        x_off = "0"
    return (
        f",scale=w='{w}*{zoom}':h='{h}*{zoom}':eval=frame:flags=bicubic,"
        f"crop={w}:{h}:'(iw-{w})/2 + {x_off}':'(ih-{h})/2':exact=1"
    )


def vf_9x16(kind, amount, dur):
    motion = motion_fragment(kind, amount, dur, 1080, 1920)
    return f"scale=1080:1920:flags=lanczos{motion},{GRADE}"


def fc_16x9(kind, amount, dur):
    motion = motion_fragment(kind, amount, dur, 1920, 1080)
    return (
        "[0:v]split=2[bgsrc][crisp];"
        "[bgsrc]scale=2160:3840,crop=1920:1080:120:1380,gblur=sigma=22,"
        "eq=brightness=-0.18:saturation=0.85[bg];"
        # Crisp speaker centered: 720x1280 -> scale to fit height (607x1080) center
        "[crisp]scale=607:1080:flags=lanczos[fg];"
        f"[bg][fg]overlay={(1920-607)//2}:0[combined];"
        f"[combined]format=yuv420p{motion},{GRADE}[v]"
    )


def extract(aspect, paths_out):
    seg_dir = SEG_V if aspect == "9x16" else SEG_H
    print(f"\n=== {aspect} extract (tt V{VERSION}) ===")
    for i, r in enumerate(EDL["ranges"]):
        start, end = float(r["start"]), float(r["end"])
        dur = end - start
        beat = r["beat"]
        kind, amount = MOTION.get(beat, ("hold", 0))
        out = seg_dir / f"seg_{i:02d}_{beat}.mp4"
        if aspect == "9x16":
            cmd_v = ["-vf", vf_9x16(kind, amount, dur)]
        else:
            cmd_v = ["-filter_complex", fc_16x9(kind, amount, dur),
                     "-map", "[v]", "-map", "0:a"]
        af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0,dur-0.03):.3f}:d=0.03"
        cmd = ["ffmpeg", "-y", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
               "-i", str(SRC), *cmd_v, "-af", af,
               "-c:v", "libx264", "-preset", "fast", "-crf", "20",
               "-pix_fmt", "yuv420p", "-r", str(FPS),
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
               "-movflags", "+faststart", "-shortest", str(out)]
        if aspect == "9x16":
            # 9:16 is simpler; keep map default
            pass
        print(f"  [{i:02d}] {beat:<12} {start:6.2f}-{end:6.2f} ({dur:4.2f}s) {kind}")
        p = subprocess.run(cmd, capture_output=True)
        if p.returncode != 0:
            print(p.stderr.decode(errors="replace")[-2500:])
            raise RuntimeError("extract failed")
        paths_out.append(out)


def concat(paths, out_path):
    listfile = out_path.parent / f"_concat_{out_path.stem}.txt"
    listfile.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in paths), encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
           "-c", "copy", "-movflags", "+faststart", str(out_path)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    listfile.unlink(missing_ok=True)


def main():
    t0 = time.time()
    pv, ph = [], []
    extract("9x16", pv)
    extract("16x9", ph)
    concat(pv, BASE_V)
    concat(ph, BASE_H)
    for p in (BASE_V, BASE_H):
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nk=1:nw=1", str(p)]
        d = float(subprocess.check_output(cmd).decode().strip())
        print(f"  {p.name}: {d:.2f}s")
    print(f"  total {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
