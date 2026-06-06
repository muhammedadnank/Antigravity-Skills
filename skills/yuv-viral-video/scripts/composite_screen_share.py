"""V7 composite for 0423 — uses screen-content-first base (top 2/3 dashboard +
bottom 1/3 rounded speaker PIP). Places Apple-glass cards on top of the screen
content area as floating callouts. Does NOT replace screen content with dark BG.
Saves output with _V7 suffix.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

EDIT = Path(r"C:\Users\User\Desktop\edit")
BASE_VERSION = 8
OUT_VERSION = 8
BASE_V = EDIT / f"base_9x16_V{BASE_VERSION}.mp4"
BASE_H = EDIT / f"base_16x9_V{BASE_VERSION}.mp4"
SUBS_V = EDIT / "karaoke.ass"
SUBS_H = EDIT / "karaoke_16x9.ass"
SFX = EDIT / "sfx"
FINAL_V = EDIT / f"final_9x16_V{OUT_VERSION}.mp4"
FINAL_H = EDIT / f"final_16x9_V{OUT_VERSION}.mp4"

edl = json.loads((EDIT / "edl.json").read_text(encoding="utf-8"))
offsets = []
acc = 0.0
for r in edl["ranges"]:
    offsets.append((r["beat"], acc, acc + (r["end"] - r["start"])))
    acc += r["end"] - r["start"]


def w_(name):
    for b, s, e in offsets:
        if b == name:
            return s, e


HOOK_S, HOOK_E   = w_("HOOK")
CTX_S, CTX_E     = w_("CONTEXT")
REVEAL_S, REVEAL_E = w_("REVEAL")
PLAT_S, PLAT_E   = w_("PLATFORMS")
METR_S, METR_E   = w_("METRICS")
GRAPH_S, GRAPH_E = w_("GRAPHICS")
AUTO_S, AUTO_E   = w_("AUTO")
NANO_S, NANO_E   = w_("NANO_BANANA")
WOW_S, WOW_E     = w_("WOW")
CTA_S, CTA_E     = w_("CTA")

# Reuse the v6 cards (already have apple-glass with correct content).
# These are positioned at left-half coordinates (x≈40-540 for 9x16, x≈60-1140 for 16x9).
GLASS_CARDS = [
    ("reveal.png",     "reveal_mask.png",     REVEAL_S + 0.20, REVEAL_E),
    ("platforms.png",  "platforms_mask.png",  PLAT_S + 0.20,   PLAT_E),
    ("auto.png",       "auto_mask.png",       AUTO_S + 4.00,   AUTO_E),
    ("cta.png",        "cta_mask.png",        CTA_S,           CTA_E),
]
KEY_CARDS = [
    ("km_hook.png",    "km_hook_mask.png",    HOOK_S + 0.20, HOOK_E),
    ("km_reveal.png",  "km_reveal_mask.png",  REVEAL_S,      REVEAL_E),
    ("km_metrics.png", "km_metrics_mask.png", METR_S,        METR_E),
    ("km_auto.png",    "km_auto_mask.png",    AUTO_S,        AUTO_E),
    ("km_nano.png",    "km_nano_mask.png",    NANO_S,        NANO_E),
    ("km_wow.png",     "km_wow_mask.png",     WOW_S,         WOW_E),
    ("km_cta.png",     "km_cta_mask.png",     CTA_S,         CTA_E),
]
ANIMS = [
    ("anim_metrics", METR_S,        METR_E),
    ("anim_flow",    AUTO_S + 0.10, AUTO_S + 3.7),
]
NO_GLASS_CARDS = [
    ("wow.png", WOW_S, WOW_E),
]

SFX_LIST = [
    (SFX / "impact.mp3",    HOOK_S,         0.55),
    (SFX / "bass_drop.mp3", HOOK_S,         0.50),
    (SFX / "whoosh.mp3",    HOOK_E,         0.42),
    (SFX / "whoosh.mp3",    REVEAL_S,       0.40),
    (SFX / "ding.mp3",      REVEAL_S+0.20,  0.50),
    (SFX / "whoosh.mp3",    PLAT_S,         0.40),
    (SFX / "ding.mp3",      METR_S+0.05,    0.40),
    (SFX / "ding.mp3",      METR_S+0.20,    0.40),
    (SFX / "ding.mp3",      METR_S+0.40,    0.40),
    (SFX / "ding.mp3",      METR_S+0.60,    0.40),
    (SFX / "glitch.mp3",    GRAPH_S,        0.45),
    (SFX / "whoosh.mp3",    AUTO_S,         0.40),
    (SFX / "ding.mp3",      AUTO_S+4.0,     0.45),
    (SFX / "riser.mp3",     WOW_S - 1.0,    0.50),
    (SFX / "impact.mp3",    WOW_S,          0.65),
    (SFX / "whoosh.mp3",    CTA_S,          0.42),
]


def popscale(dur):
    fade_out = max(0, dur - 0.20)
    return (
        f"if(lt(t,0.28), 0.65 + 0.45*pow(t/0.28, 0.6),"
        f" if(lt(t,0.42), 1.10 - 0.10*((t-0.28)/0.14),"
        f" if(lt(t,{fade_out:.3f}), 1.0, 1.0 - 0.05*((t-{fade_out:.3f})/0.20))))"
    )


def render_aspect(aspect):
    if aspect == "9x16":
        base, w, h = BASE_V, 1080, 1920
        cards_dir = EDIT / "cards_v6_9x16"
        subs = SUBS_V
        out = FINAL_V
    else:
        base, w, h = BASE_H, 1920, 1080
        cards_dir = EDIT / "cards_v6_16x9"
        subs = SUBS_H
        out = FINAL_H

    print(f"\n=== 0423 V{OUT_VERSION} {aspect} composite ===")

    all_glass = list(GLASS_CARDS) + list(KEY_CARDS)
    inputs = ["-i", str(base)]
    for c in all_glass:
        inputs += ["-loop", "1", "-i", str(cards_dir / c[0])]
        inputs += ["-loop", "1", "-i", str(cards_dir / c[1])]
    for a in ANIMS:
        inputs += ["-framerate", "30", "-i", str(cards_dir / a[0] / "%04d.png")]
    for c in NO_GLASS_CARDS:
        inputs += ["-loop", "1", "-i", str(cards_dir / c[0])]
    for s in SFX_LIST:
        inputs += ["-i", str(s[0])]

    glass_idx_start = 1
    anim_idx_start = glass_idx_start + 2 * len(all_glass)
    nog_idx_start = anim_idx_start + len(ANIMS)
    sfx_idx_start = nog_idx_start + len(NO_GLASS_CARDS)

    parts = []
    n_glass = len(all_glass)
    if n_glass > 0:
        parts.append("[0:v]gblur=sigma=24,format=rgba[blur_pre]")
        if n_glass == 1:
            parts.append("[blur_pre]copy[bl0]")
        else:
            so = "".join(f"[bl{i}]" for i in range(n_glass))
            parts.append(f"[blur_pre]split={n_glass}{so}")

    current = "[0:v]"

    for ci, (card_name, mask_name, st, en) in enumerate(all_glass):
        card_idx = glass_idx_start + 2 * ci
        mask_idx = glass_idx_start + 2 * ci + 1
        dur = en - st
        m_lab = f"[m{ci}]"
        parts.append(f"[{mask_idx}:v]format=gray{m_lab}")
        rb_lab = f"[rb{ci}]"
        parts.append(f"[bl{ci}]{m_lab}alphamerge{rb_lab}")
        next_lab = f"[rbase{ci}]"
        parts.append(
            f"{current}{rb_lab}overlay=0:0:enable='between(t,{st:.3f},{en:.3f})'{next_lab}"
        )
        current = next_lab
        scl = popscale(dur)
        fout = max(0, dur - 0.20)
        c_lab = f"[c{ci}]"
        out_lab = f"[v_card{ci}]"
        parts.append(
            f"[{card_idx}:v]format=rgba,setpts=PTS-STARTPTS,"
            f"scale=w='{w}*({scl})':h=-2:eval=frame:flags=bicubic,"
            f"fade=t=in:st=0:d=0.10:alpha=1,"
            f"fade=t=out:st={fout:.3f}:d=0.20:alpha=1,"
            f"setpts=PTS+{st:.3f}/TB"
            f"{c_lab}"
        )
        parts.append(
            f"{current}{c_lab}overlay=x='(W-w)/2':y='(H-h)/2':"
            f"enable='between(t,{st:.3f},{en:.3f})'{out_lab}"
        )
        current = out_lab

    for ai, (subdir, st, en) in enumerate(ANIMS):
        idx = anim_idx_start + ai
        dur = en - st
        extend = max(0, dur - 1.2)
        a_lab = f"[a{ai}]"
        out_lab = f"[v_anim{ai}]"
        parts.append(
            f"[{idx}:v]format=rgba,setpts=PTS-STARTPTS,"
            f"tpad=stop_mode=clone:stop_duration={extend:.3f},"
            f"fade=t=in:st=0:d=0.15:alpha=1,"
            f"fade=t=out:st={max(0, dur - 0.20):.3f}:d=0.20:alpha=1,"
            f"setpts=PTS+{st:.3f}/TB"
            f"{a_lab}"
        )
        parts.append(
            f"{current}{a_lab}overlay=0:0:enable='between(t,{st:.3f},{en:.3f})'{out_lab}"
        )
        current = out_lab

    for ni, (name, st, en) in enumerate(NO_GLASS_CARDS):
        idx = nog_idx_start + ni
        dur = en - st
        scl = popscale(dur)
        fout = max(0, dur - 0.20)
        n_lab = f"[n{ni}]"
        out_lab = f"[v_no{ni}]"
        parts.append(
            f"[{idx}:v]format=rgba,setpts=PTS-STARTPTS,"
            f"scale=w='{w}*({scl})':h=-2:eval=frame:flags=bicubic,"
            f"fade=t=in:st=0:d=0.10:alpha=1,"
            f"fade=t=out:st={fout:.3f}:d=0.20:alpha=1,"
            f"setpts=PTS+{st:.3f}/TB"
            f"{n_lab}"
        )
        parts.append(
            f"{current}{n_lab}overlay=x='(W-w)/2':y='(H-h)/2':"
            f"enable='between(t,{st:.3f},{en:.3f})'{out_lab}"
        )
        current = out_lab

    if subs.exists():
        ass = str(subs.resolve()).replace("\\", "/").replace(":", "\\:")
        fd = str((EDIT / "fonts").resolve()).replace("\\", "/").replace(":", "\\:")
        parts.append(f"{current}subtitles='{ass}':fontsdir='{fd}'[vout]")
    else:
        parts.append(f"{current}null[vout]")

    parts.append("[0:a]volume=1.0[a0]")
    sfx_labs = ["[a0]"]
    for i, (path, st, vol) in enumerate(SFX_LIST):
        idx = sfx_idx_start + i
        delay_ms = int(st * 1000)
        lab = f"[s{i}]"
        parts.append(
            f"[{idx}:a]volume={vol},adelay={delay_ms}|{delay_ms},apad=pad_dur=0.5{lab}"
        )
        sfx_labs.append(lab)
    parts.append(
        "".join(sfx_labs) + f"amix=inputs={len(sfx_labs)}:normalize=0:duration=first[aout]"
    )

    fc = ";".join(parts)
    prenorm = EDIT / f"_prenorm_v{OUT_VERSION}_{aspect}.mp4"
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "-shortest", str(prenorm),
    ]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        print(p.stderr.decode(errors="replace")[-3500:])
        sys.exit(1)
    cmd_ln = [
        "ffmpeg", "-y", "-i", str(prenorm),
        "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1:LRA=11",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(out),
    ]
    p = subprocess.run(cmd_ln, capture_output=True)
    if p.returncode != 0:
        print(p.stderr.decode(errors="replace")[-2000:])
        sys.exit(1)
    prenorm.unlink(missing_ok=True)
    size = out.stat().st_size / (1024 * 1024)
    print(f"  done: {out.name} ({size:.1f} MB)")


if __name__ == "__main__":
    render_aspect("9x16")
    render_aspect("16x9")
