# Transcript Review — The Pause/Approve Step

This is the critical step that makes captions PERFECT. The Whisper transcript is never
100% — especially for Hebrew product names and proper nouns. The user MUST get a chance
to fix mishears before the long final render.

## What to do

After transcribe + apply known-corrections, write `transcript_review.txt` to the project
root with the format below, then **stop and ask the user to review/edit it**.

## File format

```
# Transcript Review
# Edit the TEXT of any line. Keep the [mm:ss] prefix unchanged — that's how I re-align
# words to the original Whisper timing. Save the file when done and reply "continue".

[00:00] Hi everyone, my name is Yuval.
[00:02] I'm an AI builder and speaker.
[00:05] We're going to meet soon for a practical AI session about Claude Desktop.
...

# === CORRECTIONS APPLIED ===
# cloud → Claude (×7)
# excalibro → Excalidraw (×3)
# nice account → Anthropic account
```

Each line is one whisper segment. The `[mm:ss]` prefix is the segment start time — leave
it untouched. The user edits text only.

## The prompt to send the user

> I dumped the transcript with my corrections applied to `transcript_review.txt`.
> Open it, fix any wrong words (the Hebrew/English mishears Whisper got wrong), save it,
> and reply with **"continue"** or **"render it"**. I'll re-load the edited transcript
> and run the final render then.

## On user "continue"

1. Read `transcript_review.txt`.
2. Parse each `[mm:ss] text` line. Match each line to the original segment in
   `transcript.json` by start-time (sub-second tolerance).
3. Replace the segment's `text` with the user-edited version.
4. For the per-word `words` array of that segment: tokenise the new text into words and
   re-distribute the original word timings to the new tokens **by sequential position**.
   If the new line has fewer words than the original, drop trailing word boxes. If more,
   interpolate the extra words within the segment's start–end span by character weight.
5. Save the re-aligned transcript to `transcript.json` (overwrite).
6. Re-run `gen_body.py` against the now-correct transcript.
7. Lint, render, verify.

## Notes

- **Never skip this step** — even if you think the corrections dict is exhaustive. The
  user might want to phrase a caption differently from what was spoken (tighten, clarify).
- For multi-line review sessions (long videos), the user can do partial edits — accept
  whatever they save.
- If the user says "looks good, render" without editing — proceed; the file as written
  has the corrections already applied.
- If the user requests another correction pass after seeing the render, re-enter at the
  review step with the new transcript (don't re-transcribe).
