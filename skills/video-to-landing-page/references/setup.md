# Setup — Prerequisites for `video-to-landing-page`

Minimal install. The output is a static HTML page — no build step, no node deps required for
the page itself.

## Required

| Tool | Version | Purpose |
| ---- | ------- | ------- |
| **FFmpeg** | any recent | Frame extraction from the source video |
| **Python** | ≥ 3.8 | Running the `extract-frames.py` build helper |

## Install commands

### Windows (PowerShell)

```powershell
winget install Python.Python.3.12
winget install Gyan.FFmpeg
```

### macOS (with Homebrew)

```bash
brew install python@3.12 ffmpeg
```

### Linux

```bash
sudo apt update
sudo apt install -y python3 ffmpeg
```

## Verify

```bash
ffmpeg -version
python --version
```

## To preview the generated page

A browser is enough. For local testing:

```bash
cd landing-<videoname>
python -m http.server 8000     # then open http://localhost:8000
```

## To deploy

Any static host. Drag-and-drop the output folder onto Vercel / Netlify / Cloudflare Pages.

```bash
# Vercel CLI example
npx vercel --prod ./landing-<videoname>
```

## Browser support

The scroll-frame mechanic uses:

- CSS `position: sticky`
- `requestAnimationFrame`
- `<img>` swap

All evergreen browsers (Chrome 90+, Safari 14+, Firefox 90+, Edge 90+). Mobile works.
