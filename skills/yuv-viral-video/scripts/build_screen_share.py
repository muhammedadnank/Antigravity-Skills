"""V7 build for 0423 — REVERTED to screen-content-first layout.

For 0423 the source's screen content (Claude chat, Meta Ads dashboard, generated
images) IS the visual story. We MUST preserve it.

Layout per aspect:
  9:16 (1080x1920):
    Top 2/3 (1080x1280) = source screen content (crop+scale center 1215x1440 column)
    Bottom 1/3 (1080x640) = speaker PIP (470x460 at (2040,950) zoomed up + rounded mask)
  16:9 (1920x1080):
    Full source 2560x1440 scaled to 1920x1080. Speaker PIP from source already
    sits in bottom-right; we overlay a rounded-corner mask on that region for polish.

Layout A (HOOK only) — no screen-share. Use full speaker (centered crop 9:16) /
just-scale the source for 16:9.
"""
from __future__ import annotations
import json, subprocess, time
from pathlib import Path
from PIL import Image, ImageDraw

EDIT = Path(r"C:\Users\User\Desktop\edit")
SRC = Path(r"C:\Users\User\Desktop\0423.mp4")
EDL = json.loads((EDIT / "edl.json").read_text(encoding="utf-8"))

LAYOUT_ASSETS = EDIT / "layout_assets"
LAYOUT_ASSETS.mkdir(exist_ok=True)

SEG_V = EDIT / "segments_v7_9x16"
SEG_H = EDIT / "segments_v7_16x9"
SEG_V.mkdir(parents=True, exist_ok=True)
SEG_H.mkdir(parents=True, exist_ok=True)

# Versioned outputs to keep backups
VERSION = 8
BASE_V = EDIT / f"base_9x16_V{VERSION}.mp4"
BASE_H = EDIT / f"base_16x9_V{VERSION}.mp4"
GRADE = "eq=contrast=1.04:saturation=1.04:gamma=1.02"
FPS = 30

# 9:16 layout — speaker PIP in bottom 1/3 of frame.
# IMPORTANT: source PIP is 470x460 (~1:1 aspect). Target dims MUST preserve that
# aspect to avoid horizontal squish on the speaker.
PIP_9V = {"x": 240, "y": 1300, "w": 600,  "h": 588, "radius": 56}
# 16:9 layout — speaker PIP follows the source's existing bottom-right corner.
# Source is 2560x1440 with PIP at (~2040,950) 470x460. Scaled to 1920x1080, the
# PIP lands at approximately (1530,712) size 352x345.
PIP_16H = {"x": 1530, "y": 712, "w": 352, "h": 344, "radius": 36}


def make_pip_masks():
    for path, geom in [
        (LAYOUT_ASSETS / f"pip_v7_9x16.png", PIP_9V),
        (LAYOUT_ASSETS / f"pip_v7_16x9.png", PIP_16H),
    ]:
        m = Image.new("L", (geom["w"], geom["h"]), 0)
        ImageDraw.Draw(m).rounded_rectangle(
            [0, 0, geom["w"], geom["h"]], radius=geom["radius"], fill=255)
        m.save(path)
    print("  PIP masks regenerated")


# Per-beat motion (subtle)
MOTION = {
    "HOOK":         ("push_in",  0.06),
    "CONTEXT":      ("dolly_l",  0.04),
    "REVEAL":       ("snap_in",  0.05),
    "PLATFORMS":    ("hold",     0.0),
    "METRICS":      ("push_in",  0.04),
    "GRAPHICS":     ("snap_in",  0.04),
    "AUTO":         ("pull_out", 0.05),
    "NANO_BANANA":  ("push_in",  0.04),
    "WOW":          ("snap_in",  0.10),
    "CTA":          ("push_in",  0.04),
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


# ----- 9:16 filter complex -----
def fc_9x16(layout, kind, amount, dur):
    motion_top = motion_fragment(kind, amount, dur, 1080, 1280)
    if layout == "A":
        # Full-frame speaker — fill whole canvas vertically
        return (
            f"[0:v]crop=810:1440:875:0,scale=1080:1920{motion_top.replace('1280','1920')},"
            f"{GRADE}[v]"
        )
    # Layout B: top = screen content, bottom = speaker PIP (rounded)
    pip = PIP_9V
    return (
        # split source for top + pip
        "[0:v]split=2[srctop][srcpip];"
        # Top 2/3: crop center column 1215x1440 of source, scale to 1080x1280, motion
        f"[srctop]crop=1215:1440:660:0,scale=1080:1280{motion_top},{GRADE}[top];"
        # PIP: crop 470x460 at (2040,950), scale up to PIP target
        f"[srcpip]crop=470:460:2040:950,scale={pip['w']}:{pip['h']}:flags=lanczos,"
        f"{GRADE}[pip_raw];"
        # Round corners with mask
        "[1:v]format=gray[pip_alpha];"
        "[pip_raw][pip_alpha]alphamerge[pip_rounded];"
        # Compose: dark fill bottom strip + top + pip
        # Build final 1080x1920 canvas: top (0,0)1080x1280 + dark below + pip
        # Use color filter for the bottom dark strip
        "color=c=0x0c0e16:size=1080x1920:r=30,trim=duration=" + f"{dur:.3f}[bg];"
        f"[bg][top]overlay=0:0[bgtop];"
        f"[bgtop][pip_rounded]overlay={pip['x']}:{pip['y']}[v]"
    )


# ----- 16:9 filter complex -----
def fc_16x9(layout, kind, amount, dur):
    motion = motion_fragment(kind, amount, dur, 1920, 1080)
    if layout == "A":
        return (
            f"[0:v]crop=2520:1417:20:11,scale=1920:1080{motion},{GRADE}[v]"
        )
    # Layout B: scale source 2560x1440 -> 1920x1080. PIP in source naturally
    # appears at (~1530,712) after scale. Apply rounded mask on that region.
    # Motion would break the PIP-mask alignment so we skip it for layout B.
    pip = PIP_16H
    return (
        f"[0:v]scale=1920:1080:flags=lanczos,{GRADE},split=2[full_main][full_for_pip];"
        f"[full_for_pip]crop={pip['w']}:{pip['h']}:{pip['x']}:{pip['y']}[pip_raw];"
        "[1:v]format=gray[pip_alpha];"
        "[pip_raw][pip_alpha]alphamerge[pip_rounded];"
        f"[full_main][pip_rounded]overlay={pip['x']}:{pip['y']}[v]"
    )


def extract(aspect, paths_out):
    seg_dir = SEG_V if aspect == "9x16" else SEG_H
    mask_path = LAYOUT_ASSETS / f"pip_v7_{aspect}.png"
    print(f"\n=== {aspect} extract (0423 V{VERSION}) ===")
    for i, r in enumerate(EDL["ranges"]):
        start, end = float(r["start"]), float(r["end"])
        dur = end - start
        beat = r["beat"]
        layout = r.get("layout", "A")
        kind, amount = MOTION.get(beat, ("hold", 0))
        out = seg_dir / f"seg_{i:02d}_{beat}.mp4"
        if aspect == "9x16":
            fc = fc_9x16(layout, kind, amount, dur)
        else:
            fc = fc_16x9(layout, kind, amount, dur)
        af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0,dur-0.03):.3f}:d=0.03"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(SRC),
            "-loop", "1", "-t", f"{dur:.3f}", "-i", str(mask_path),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "0:a",
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", "-shortest", str(out),
        ]
        print(f"  [{i:02d}] {beat:<12} {start:6.2f}-{end:6.2f} ({dur:4.2f}s)  layout={layout}  {kind}")
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
    make_pip_masks()
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
