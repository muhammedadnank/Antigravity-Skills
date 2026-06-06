"""Pre-render shared layout assets used by both video pipelines:
  bg_9x16.png / bg_16x9.png         — dark gradient + soft speaker shadow
  speaker_mask_9x16.png / 16x9.png   — rounded rect alpha for the speaker card
"""
from pathlib import Path
import sys
sys.path.insert(0, r"C:\Users\User\Desktop\edit")
from apple_glass import (make_dark_bg, make_pip_mask_local,
                         SPEAKER_9X16, SPEAKER_16X9)

EDIT = Path(r"C:\Users\User\Desktop\edit") / "layout_assets"
EDIT.mkdir(parents=True, exist_ok=True)


def main():
    # 9:16 dark BG with speaker-shaped shadow
    bg = make_dark_bg(1080, 1920, (
        SPEAKER_9X16["x"], SPEAKER_9X16["y"],
        SPEAKER_9X16["w"], SPEAKER_9X16["h"],
        SPEAKER_9X16["radius"],
    ))
    bg.save(EDIT / "bg_9x16.png")

    bg = make_dark_bg(1920, 1080, (
        SPEAKER_16X9["x"], SPEAKER_16X9["y"],
        SPEAKER_16X9["w"], SPEAKER_16X9["h"],
        SPEAKER_16X9["radius"],
    ))
    bg.save(EDIT / "bg_16x9.png")

    # Speaker masks (sized to the speaker card itself)
    m = make_pip_mask_local(SPEAKER_9X16["w"], SPEAKER_9X16["h"], SPEAKER_9X16["radius"])
    m.save(EDIT / "speaker_mask_9x16.png")
    m = make_pip_mask_local(SPEAKER_16X9["w"], SPEAKER_16X9["h"], SPEAKER_16X9["radius"])
    m.save(EDIT / "speaker_mask_16x9.png")

    for p in sorted(EDIT.glob("*.png")):
        print(f"  {p.name}: {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
