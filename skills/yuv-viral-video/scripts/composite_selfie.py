"""V5 composite for tt.mp4 — full-frame speaker base + Apple-glass cards as
floating callouts. Uses v4 cards (left-half positioned, content-accurate).
Saves with _V5 suffix.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

EDIT = Path(r"C:\Users\User\Downloads\tt_edit")
SFX = Path(r"C:\Users\User\Desktop\edit\sfx")
FONTS = Path(r"C:\Users\User\Desktop\edit\fonts")

BASE_VERSION = 5
OUT_VERSION = 6  # increment per render to keep backups
BASE_V = EDIT / f"base_9x16_V{BASE_VERSION}.mp4"
BASE_H = EDIT / f"base_16x9_V{BASE_VERSION}.mp4"
SUBS_V = EDIT / "karaoke.ass"
SUBS_H = EDIT / "karaoke_16x9.ass"
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


HOOK_S, HOOK_E       = w_("HOOK")
WORK_S, WORK_E       = w_("WORKSHOP")
STUD_S, STUD_E       = w_("STUDENT")
BUILD_S, BUILD_E     = w_("BUILD_15MIN")
RES_S, RES_E         = w_("RESULT")
NOPAY_S, NOPAY_E     = w_("NO_PAY")
MAGIC_S, MAGIC_E     = w_("MAGIC")
CTA_S, CTA_E         = w_("CTA")

GLASS_CARDS = [
    ("hook.png",        "hook_mask.png",        HOOK_S + 0.05,  HOOK_E),
    ("workshop.png",    "workshop_mask.png",    WORK_S + 0.10,  WORK_E),
    ("student.png",     "student_mask.png",     STUD_S + 1.4,   STUD_E),
    ("build_15min.png", "build_15min_mask.png", BUILD_S,        BUILD_E),
    ("result.png",      "result_mask.png",      RES_S + 1.0,    RES_E),
    ("no_pay.png",      "no_pay_mask.png",      NOPAY_S,        NOPAY_E),
    ("cta.png",         "cta_mask.png",         CTA_S,          CTA_E),
]
KEY_CARDS = [
    ("km_hook.png",      "km_hook_mask.png",      HOOK_S + 0.10,  HOOK_E),
    ("km_workshop.png",  "km_workshop_mask.png",  WORK_S,         WORK_E),
    ("km_build.png",     "km_build_mask.png",     BUILD_S,        BUILD_E),
    ("km_result.png",    "km_result_mask.png",    RES_S,          RES_E),
    ("km_nopay.png",     "km_nopay_mask.png",     NOPAY_S,        NOPAY_E),
    ("km_magic.png",     "km_magic_mask.png",     MAGIC_S,        MAGIC_E),
    ("km_cta.png",       "km_cta_mask.png",       CTA_S,          CTA_E),
]
NO_GLASS_CARDS = [("magic.png", MAGIC_S, MAGIC_E)]
SFX_LIST = [
    (SFX / "impact.mp3",    HOOK_S,           0.55),
    (SFX / "bass_drop.mp3", HOOK_S,           0.50),
    (SFX / "whoosh.mp3",    HOOK_E,           0.42),
    (SFX / "whoosh.mp3",    WORK_S,           0.40),
    (SFX / "ding.mp3",      WORK_S + 0.15,    0.42),
    (SFX / "whoosh.mp3",    STUD_S,           0.42),
    (SFX / "ding.mp3",      STUD_S + 1.4,     0.50),
    (SFX / "glitch.mp3",    BUILD_S,          0.45),
    (SFX / "ding.mp3",      RES_S + 1.0,      0.45),
    (SFX / "whoosh.mp3",    NOPAY_S,          0.40),
    (SFX / "ding.mp3",      NOPAY_S + 0.05,   0.50),
    (SFX / "riser.mp3",     MAGIC_S - 0.5,    0.40),
    (SFX / "impact.mp3",    MAGIC_S,          0.55),
    (SFX / "whoosh.mp3",    CTA_S,            0.42),
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
        cards_dir = EDIT / "cards_v4_9x16"
        subs = SUBS_V
        out = FINAL_V
    else:
        base, w, h = BASE_H, 1920, 1080
        cards_dir = EDIT / "cards_v4_16x9"
        subs = SUBS_H
        out = FINAL_H

    print(f"\n=== tt V{OUT_VERSION} {aspect} composite ===")
    all_glass = list(GLASS_CARDS) + list(KEY_CARDS)

    inputs = ["-i", str(base)]
    for c in all_glass:
        inputs += ["-loop", "1", "-i", str(cards_dir / c[0])]
        inputs += ["-loop", "1", "-i", str(cards_dir / c[1])]
    for c in NO_GLASS_CARDS:
        inputs += ["-loop", "1", "-i", str(cards_dir / c[0])]
    for s in SFX_LIST:
        inputs += ["-i", str(s[0])]

    glass_idx_start = 1
    nog_idx_start = glass_idx_start + 2 * len(all_glass)
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
        fd = str(FONTS.resolve()).replace("\\", "/").replace(":", "\\:")
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
