# Setup — Prerequisites for the `video-edit` skill

This skill orchestrates several external tools. A fresh machine needs the following one-time
installs. The skill itself just calls these CLIs; nothing else is bundled.

## Required

| Tool | Version | Purpose |
| ---- | ------- | ------- |
| **Node.js** | ≥ 22 | `npx hyperframes …` (scaffold, lint, render, background-remove) |
| **Python** | ≥ 3.10 | Whisper transcription + caption generator + review scripts |
| **FFmpeg** | any recent | Audio extraction, frame extraction, footage re-encoding |
| **faster-whisper** | latest | Word-level transcription (Python package) |

## Install commands

### Windows (PowerShell, with `winget`)

```powershell
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Gyan.FFmpeg
pip install faster-whisper
```

### macOS (with Homebrew)

```bash
brew install node@22 python@3.12 ffmpeg
pip3 install faster-whisper
```

### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt install -y nodejs
pip3 install faster-whisper
```

## Verify

```bash
node --version          # v22+ expected
python --version        # 3.10+ expected
ffmpeg -version         # any recent build
python -c "import faster_whisper; print(faster_whisper.__version__)"
npx hyperframes doctor  # checks Chrome / FFmpeg / memory for renders
```

## Optional but recommended

### GPU acceleration for Whisper

faster-whisper can run on CUDA, but on Windows it usually crashes mid-decode because cuDNN is
not on the PATH. The bundled `transcribe.py` is hard-coded to CPU `int8` for that reason —
fast enough on a modern CPU (~5 min for a 3-minute clip with the large-v3 model). If you have
cuDNN properly installed on Linux, swap `device="cpu"` for `device="cuda"` and
`compute_type="int8"` for `compute_type="float16"`.

### GPU for background removal (`npx hyperframes remove-background`)

CoreML (macOS), CUDA (Linux with proper drivers) or DirectML (Windows) accelerate the u2net
mask model. Without GPU it falls back to CPU — a 10-second 1440p clip takes ~3-8 minutes.

```bash
npx hyperframes remove-background --info  # lists available execution providers
```

### Pre-cache Whisper model

The first transcribe downloads the `large-v3` model (~3 GB) into
`~/.cache/huggingface/hub/`. Subsequent runs are instant to start.

## Where files live

The skill expects to operate inside a HyperFrames project directory created by
`npx hyperframes init`. Reference assets in this skill (`references/`) are copied into that
project as part of step 4–6 in the main `SKILL.md` workflow.
