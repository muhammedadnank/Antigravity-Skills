# Codex OAuth vs OpenAI API key for baoyu-imagine

`baoyu-imagine --provider openai` uses the standard OpenAI Images API and requires `OPENAI_API_KEY`. It calls OpenAI-compatible image endpoints such as `/images/generations` and `/images/edits`.

Codex / ChatGPT login is different. Codex image generation is driven by Codex OAuth and the Codex runtime's `image_gen` capability, not by the public OpenAI Images API key path. A Codex OAuth token is not a drop-in replacement for `OPENAI_API_KEY`, and setting `OPENAI_BASE_URL` to a Codex backend will not make baoyu-imagine's existing `openai` provider work because the auth, route, and payload shape differ.

## What to use instead

- If running inside Codex and the native `imagegen` skill/tool is available, use it directly.
- If running outside Codex but the `codex` CLI is installed and logged in, use the repo-level `scripts/codex-imagegen.sh` wrapper when the calling skill supports it. The wrapper invokes `codex exec` and the Codex `image_gen` tool; no `OPENAI_API_KEY` is required.
- If running inside Hermes and a native `image_generate` tool is available, use that as a runtime-native fallback. Be explicit about whether reference images are passed directly or only reconstructed from extracted traits.
- If the user wants `baoyu-imagine` itself to support Codex OAuth, add a distinct provider such as `openai-codex` rather than modifying the existing `openai` provider.

## Reference-image prompting note

When using actual reference images for identity preservation, avoid long generic descriptions of the subject. Long descriptions can cause the model to synthesize a new similar-looking person/object. Prefer direct wording:

> Use the person/object in the reference image(s) as the same identity. Do not redesign it or create a similar-looking new subject. Only change scene, clothing, pose, lighting, rendering style, and composition.
