#!/usr/bin/env python3
"""
extract_frames.py — Probe a video, extract every frame at near-lossless
JPEG quality into <output_folder>/frame-NNN.jpg, and print a JSON
metadata block to stdout for the page generator to consume.

Usage:
    python extract_frames.py <video_path> <output_folder>
        [--target-px-per-frame N]    # default 28; used to derive scrollBudget
        [--padding N]                # default 3; zero-pad width for frame index

Requires `ffmpeg` and `ffprobe` on PATH.

The output JSON looks like:
    {
      "slug":                  "hope",
      "video_path":            "C:/.../hope.mp4",
      "output_folder":         "C:/.../hope",
      "frame_count":           241,
      "width":                 1280,
      "height":                720,
      "fps":                   24.0,
      "duration_seconds":      10.04,
      "suggested_scroll_budget": 6300,
      "padding":               3,
      "frame_naming":          "frame-001.jpg .. frame-241.jpg",
      "preview_frames": {
        "first": "frame-001.jpg",
        "mid":   "frame-121.jpg",
        "last":  "frame-241.jpg"
      },
      "total_size_bytes":      53842117
    }
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def die(msg: str, code: int = 1) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def require(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        die(f"{tool!r} not found on PATH. Install ffmpeg (which ships with ffprobe) and retry.")
    return path


def probe(video_path: Path) -> dict:
    """ffprobe → dict of width, height, fps, duration, nb_frames."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration",
        "-of", "json",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        die(f"ffprobe failed: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    streams = data.get("streams") or []
    if not streams:
        die(f"No video stream found in {video_path}")
    s = streams[0]
    fps_num, _, fps_den = s.get("r_frame_rate", "0/1").partition("/")
    try:
        fps = float(fps_num) / float(fps_den) if fps_den else float(fps_num)
    except (ValueError, ZeroDivisionError):
        fps = 0.0
    try:
        duration = float(s.get("duration", 0.0))
    except (TypeError, ValueError):
        duration = 0.0
    nb_frames_raw = s.get("nb_frames")
    nb_frames = int(nb_frames_raw) if nb_frames_raw and nb_frames_raw.isdigit() else None
    return {
        "width": int(s.get("width", 0)),
        "height": int(s.get("height", 0)),
        "fps": fps,
        "duration": duration,
        "nb_frames_hint": nb_frames,  # may be None — confirm by counting after extract
    }


def extract(video_path: Path, output_folder: Path, padding: int) -> int:
    """Run ffmpeg, return the count of extracted frame-*.jpg files."""
    output_folder.mkdir(parents=True, exist_ok=True)
    # Clear any prior frame-*.jpg so a re-run is deterministic.
    for old in output_folder.glob("frame-*.jpg"):
        try:
            old.unlink()
        except OSError:
            pass

    pattern = output_folder / f"frame-%0{padding}d.jpg"
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(video_path),
        "-q:v", "2",           # near-lossless JPEG (1=best, 31=worst)
        "-start_number", "1",
        str(pattern),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        die(f"ffmpeg failed: {result.stderr.strip()}")

    frames = sorted(output_folder.glob("frame-*.jpg"))
    if not frames:
        die("ffmpeg produced no frames — was the video readable?")
    return len(frames)


def scroll_budget(frame_count: int, px_per_frame: int) -> int:
    """Clamp to [2500, 8000] to keep both very-short and very-long clips usable."""
    raw = frame_count * px_per_frame
    return max(2500, min(8000, raw))


def total_size(folder: Path) -> int:
    return sum(f.stat().st_size for f in folder.glob("frame-*.jpg"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract HD frames from a video for a parallax landing page.")
    ap.add_argument("video", type=Path, help="Path to source video (mp4, mov, mkv, etc.)")
    ap.add_argument("output", type=Path, help="Folder to write frame-NNN.jpg into (created if missing)")
    ap.add_argument("--target-px-per-frame", type=int, default=28,
                    help="Pixels of scroll per frame; used to derive scrollBudget. Default 28.")
    ap.add_argument("--padding", type=int, default=3,
                    help="Zero-padding width for frame index. Default 3.")
    args = ap.parse_args()

    require("ffmpeg")
    require("ffprobe")

    video_path: Path = args.video.resolve()
    if not video_path.is_file():
        die(f"Video not found: {video_path}")

    output_folder: Path = args.output.resolve()

    info = probe(video_path)
    frame_count = extract(video_path, output_folder, args.padding)
    sb = scroll_budget(frame_count, args.target_px_per_frame)

    pad = args.padding
    last = frame_count
    mid = max(1, (frame_count + 1) // 2)

    out = {
        "slug": output_folder.name,
        "video_path": str(video_path).replace("\\", "/"),
        "output_folder": str(output_folder).replace("\\", "/"),
        "frame_count": frame_count,
        "width": info["width"],
        "height": info["height"],
        "fps": round(info["fps"], 3),
        "duration_seconds": round(info["duration"], 3),
        "suggested_scroll_budget": sb,
        "padding": pad,
        "frame_naming": f"frame-{str(1).zfill(pad)}.jpg .. frame-{str(last).zfill(pad)}.jpg",
        "preview_frames": {
            "first": f"frame-{str(1).zfill(pad)}.jpg",
            "mid":   f"frame-{str(mid).zfill(pad)}.jpg",
            "last":  f"frame-{str(last).zfill(pad)}.jpg",
        },
        "total_size_bytes": total_size(output_folder),
        "notes": (
            "JPEGs at q:v 2 (near-lossless). Source dimensions preserved — no up/downscale. "
            "If the result is heavy and you don't need maximum sharpness, re-run a "
            "downstream `mogrify -quality 85 frame-*.jpg` or re-extract with -q:v 3."
        ),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
