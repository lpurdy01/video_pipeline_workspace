# Agent Tools

Small command-line helpers for delegating review and planning work to Gemini
without loading generated media into the assistant context.

Approved by the workspace rules:

- generated visual artifacts, including frames and prototype stills;
- text artifacts from this project, including scripts, summaries, prompts,
  rewrite plans, and article drafts;
- scratch/demo narration text.

Not approved by default:

- raw human voice recordings;
- human narration audio chunks;
- voiceprints, speaker embeddings, or timing-rich human narration artifacts.

Generated tool output belongs under `agent_tools/out/`, which is git-ignored.

## Focused Frame Review

```bash
python3 representation_transform_visuals/agent_tools/ask_gemini_about_frame.py \
  --frame representation_transform_visuals/manifest_pipeline/out/review_frames/01_01_opening_start.png \
  --question "Does the highlighted object match the narration at this moment?"
```

## Text Planning / Critique

```bash
python3 representation_transform_visuals/agent_tools/ask_gemini_text.py \
  --prompt "Review this animation workflow and suggest failure-proof synchronization checks." \
  --context-file representation_transform_visuals/drafts/workflow_plan_2026_05_31.md
```

## Deep Research

Use this for background research or complex planning that benefits from a
long-running Gemini agent.

```bash
python3 representation_transform_visuals/agent_tools/ask_deep_research.py \
  --prompt-file representation_transform_visuals/drafts/tech_tree_research_prompt.md \
  --submit

python3 representation_transform_visuals/agent_tools/ask_deep_research.py --poll
```
