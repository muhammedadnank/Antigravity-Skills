"""Extract evenly-spaced frames from a video for the scroll-driven landing page.

Usage:
    python extract-frames.py <video> <output_dir> [count]
    python extract-frames.py <video> <output_dir> [count] --build-html

Examples:
    python extract-frames.py demo.mp4 landing-demo
    python extract-frames.py demo.mp4 landing-demo 120 --build-html
"""

import json, os, subprocess, sys, shutil

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

VIDEO = sys.argv[1]
OUT_DIR = sys.argv[2]
COUNT = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 80
BUILD_HTML = "--build-html" in sys.argv

# Probe duration
probe = subprocess.run(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        VIDEO,
    ],
    capture_output=True, text=True, check=True,
)
duration = float(probe.stdout.strip())

frames_dir = os.path.join(OUT_DIR, "frames")
os.makedirs(frames_dir, exist_ok=True)

# Extract N evenly-spaced frames at quality 2 (JPG ~q82), downscaled to max 1920 wide.
print(f"Extracting {COUNT} frames from {VIDEO} ({duration:.1f}s)...")
for i in range(COUNT):
    t = (i + 0.5) * duration / COUNT  # midpoint of each segment
    out_path = os.path.join(frames_dir, f"f_{i+1:04d}.jpg")
    subprocess.run(
        [
            "ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", VIDEO,
            "-vframes", "1",
            "-vf", "scale='min(1920,iw)':-2",
            "-q:v", "3",
            out_path,
        ],
        capture_output=True, check=True,
    )
print(f"Wrote {COUNT} frames to {frames_dir}/")

if BUILD_HTML:
    # Locate landing-template.html (sibling to this script)
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "landing-template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    frame_tags = "\n      ".join(
        f'<img class="frame{" active" if i == 0 else ""}" loading="eager" src="frames/f_{i+1:04d}.jpg" data-i="{i}" alt="" />'
        for i in range(COUNT)
    )
    html = html.replace("__FRAMES__", frame_tags)
    html = html.replace("__FRAME_COUNT__", str(COUNT))
    out_html = os.path.join(OUT_DIR, "index.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_html}")
    print("Customise the placeholders: __HEADLINE__, __TAGLINE__, __CTA_TEXT__, __CTA_HREF__")
