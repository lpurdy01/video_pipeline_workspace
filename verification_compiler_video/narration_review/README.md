# Narration Review Workflow

This workflow is for the review process where the user records a read-through
of the script and adds spoken commentary about what feels wrong, how they would
say a line, or what should change.

Raw human voice stays local by default.

## Recommended Recording Pattern

Record one of these:

1. **Full read-through plus comments**
   - Read the current script.
   - When something feels wrong, pause and say `COMMENT:`.
   - Explain the issue in natural speech.
   - Resume reading.

2. **Section-by-section review**
   - Record one file per section.
   - Use filenames like `review_01_generation_got_cheap.wav`.
   - This is easier to align to the script.

3. **Free-form rewrite commentary**
   - Talk through the whole idea without reading every line.
   - Useful when the structure is wrong rather than individual wording.

## Spoken Comment Conventions

Use simple verbal markers so local transcription can be converted into review
notes later:

```text
COMMENT: this line feels too formal
REWRITE: I would say it like this ...
CUT: remove the standards caveat here
MOVE: this belongs after the graph section
KEEP: this phrasing is good
ALT HOOK: what if the opening was ...
```

These markers are intentionally plain. The transcript parser can find them
without needing word-perfect alignment.

## Local Transcription

Use the existing local transcription tool from the representation-transform
workflow:

```bash
python3 representation_transform_visuals/narration_pipeline/transcribe_words.py \
  --audio verification_compiler_video/assets/human_audio/readthrough_YYYY_MM_DD.wav \
  --out verification_compiler_video/narration_review/out/readthrough_YYYY_MM_DD.words.json
```

Then produce a readable transcript from the local word JSON or use the transcript
text directly in review notes. Do not upload the raw audio, word timestamps, or
timing-rich voice artifacts unless explicitly approved for that request.

## Bulk Review Editing Loop

1. Record read-through/commentary audio locally.
2. Transcribe locally.
3. Save transcript text under `narration_review/out/`.
4. Convert marked comments into `review_notes_YYYY_MM_DD.md`.
5. Apply script edits in bulk.
6. Update `drafts/script.md`.
7. Rebuild any script chunks or manifest sections affected by the changes.

## Review Note Format

Use this structure for each comment:

```text
## Comment N

Section:
Marker:
Transcript excerpt:
Interpretation:
Suggested edit:
Status: open | applied | rejected | needs discussion
```

