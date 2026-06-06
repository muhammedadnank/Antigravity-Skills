# HyperFrames Transcript Editor

Interactive, **browser-only** editor for fixing speech-to-text mishears before the final
render. Designed for the `video-edit` skill but works standalone with any transcript.json
that follows the faster-whisper word-level format.

## What it does

- **One-click project folder load** — point at a HyperFrames project directory and the
  editor auto-finds `transcript.json` + the source/footage video, opens itself, and saves
  `transcript_review.txt` back to the same folder when you hit Save (uses the File System
  Access API; Chrome/Edge 86+, Safari 15.2+; falls back to individual file pickers and a
  download on unsupported browsers).
- Loads a `transcript.json` (word-level whisper output) and a source video — entirely in
  the browser, zero upload.
- Renders each segment as an inline-editable textarea with the timecode prefix.
- Clicking a segment seeks the video to that moment; the active segment auto-highlights as
  the video plays.
- Auto-saves edits to `localStorage` so refreshes don't lose work.
- Supports **Hebrew RTL** (per-segment `direction: auto`).
- One-click **dictionary corrections** (paste `{wrong: right}` JSON, whole-word match).
- One-click **find / replace** across all segments.
- **Optional WebLLM AI suggestions** — runs Qwen2.5-3B or Llama-3.2-3B in the browser via
  WebGPU. First load downloads the model (~1–2 GB, cached forever after). Each segment
  gets a 🤖 button that asks the LLM to fix Whisper mishears given previous/next-line
  context, then surfaces an accept/dismiss inline diff.
- Saves a `transcript_review.txt` in the exact format the skill's `apply_review.py`
  expects — drop it back in the project and the agent re-aligns word timings + re-renders.

## How to open

```bash
# From the video-edit skill directory:
start ./transcript-editor/index.html       # Windows
open ./transcript-editor/index.html        # macOS
xdg-open ./transcript-editor/index.html    # Linux

# Or run a quick HTTP server (recommended for WebGPU/WebLLM)
cd transcript-editor && python -m http.server 8765
# then open http://localhost:8765
```

WebLLM needs **WebGPU** support — Chrome / Edge 113+, Safari TP. Firefox stable still
lacks WebGPU by default; flip `dom.webgpu.enabled` in `about:config` if you must.

## Keyboard shortcuts

| Key | Action |
| --- | ------ |
| `Space` | Play / pause video |
| `Cmd/Ctrl + S` | Save `transcript_review.txt` |

## Workflow with the `video-edit` skill

1. Agent runs `transcribe.py` → produces `transcript.json`.
2. Agent runs `make_review.py` (applies known corrections, writes `transcript_review.txt`).
3. Instead of editing the .txt in Notepad, you open this editor, load the `transcript.json`
   and source video, fix everything visually with timing + video preview + AI suggestions,
   and save the new `transcript_review.txt`.
4. Tell the agent **"continue"** — it runs `apply_review.py` to redistribute word timings
   into `transcript.json`, regenerates the caption sub-composition, and re-renders.

## Standalone use

The editor doesn't need the agent. Drop any whisper JSON + matching video, edit, save.
The output is a flat `[mm:ss.xx] text` file you can copy into your own workflow.

## Privacy

Everything runs in your browser. No telemetry. WebLLM model files download from the
MLC-AI CDN on first use only; nothing about your transcript leaves your machine.
