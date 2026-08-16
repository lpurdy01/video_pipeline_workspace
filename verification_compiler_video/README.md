# Verification Compiler Video

This folder is the production workspace for a short explainer video about the
Verification Compiler.

Working title:

**The Compiler For Trust**

Core spine:

```text
generation got cheap -> verification bottleneck -> artifact graph
-> deterministic traversal -> verification query package -> evidence record
-> readiness map
```

This project is separate from `representation_transform_visuals/`. It reuses
the production lessons from that workstream, but the subject, script, assets,
and review artifacts live here.

## Current Files

- `drafts/script.md`: first-pass narration script for the 10-minute video.
- `drafts/storyboard.md`: section-by-section visual and narration beat plan.
- `production_manifest.json`: section manifest for script chunks, visual source
  selection, review frames, and human recording checklist.
- `manim_prototypes/`: rough Manim scenes for every main section.
- `narration_review/`: workflow for recording human read-through commentary and
  turning local transcripts into review notes.
- `assets/human_audio/`: local human narration/commentary recordings.

## Human Audio Policy

Keep raw human audio local by default. Do not upload human voice recordings,
voiceprints, speaker embeddings, or timing-rich human narration artifacts to
Gemini or another cloud API unless there is explicit per-request approval.

Text artifacts, scripts, transcript text, commentary summaries, review notes,
and generated visual artifacts are approved for Gemini review under the current
repo policy.

## First Prototype Target

The first visual prototype should prove that the following beats read clearly:

1. artifact flood into verification gate;
2. chat transcript failing as evidence;
3. traceability chain;
4. artifact graph;
5. deterministic traversal beam;
6. VQP fold/open;
7. dual-mode review;
8. evidence card staleness;
9. readiness heat map;
10. human decision surface.

Run the rough Manim scenes with:

```bash
bash verification_compiler_video/manim_prototypes/render_storyboard_sections.sh
```

