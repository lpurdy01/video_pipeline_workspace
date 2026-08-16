# Workflow improvement plan — 2026-05-31

Long-running task. User asked for 4 workflow improvements before next sync.
Done in priority order with status tracked here for context safety.

## Priority 1: Gemini-default frame review + Gemini-delegated research

**Goal**: Stop reading PNG frames into my own context. Route all frame
review through Gemini (existing pipeline) and read only the markdown reply.
Also use existing Gemini agents (deep-research, etc.) for complex
research/planning subtasks.

**Status**: implemented locally; Deep Research completed

**Steps**:
- [x] Audit existing Gemini infrastructure in this repo
  - `whitepaper/gemini_tools/` (gemini_client.py, whitepaper_review.py, diagram_render.py)
  - `image_review_pipeline/review_keyframes.py` (current frame review)
  - `manifest_pipeline/review_manifest_build.py` (dense review wrapper)
- [x] Add a small "ask_gemini_about_frame" helper that takes a frame path + a focused question and returns the answer. Saves me from reading frames for spot-checks.
- [x] Add a "ask_deep_research" helper that delegates a research question to `deep-research-max-preview-04-2026`. Use for tech-tree lineage, etc.
- [x] Add `ask_gemini_text.py` for text-only planning / critique.
- [x] Document the new helpers in a README so future-me doesn't forget.
- [x] Ask Gemini for workflow guardrails; saved to ignored `agent_tools/out/workflow_guardrails_gemini.md`.
- [x] Submit tech-tree lineage research prompt to Gemini Deep Research; state saved to ignored `agent_tools/out/deep_research_state.json`.
- [x] Poll Deep Research to completion; report saved to ignored `agent_tools/out/deep_research_report.md`.
- [x] Use focused Gemini frame review for repaired target frames instead of loading PNGs into assistant context.
- [ ] Run follow-up Gemini review for S04/S06/S11 readability repairs after usage limit resets. Last attempt was blocked by the usage-limit approval gate, so this remains intentionally pending rather than worked around.

## Priority 2: Word-level audio alignment

**Goal**: Manim scenes anchor visual beats to phrases in narration, not
arbitrary `wait(N)` seconds.

**Status**: implemented for scratch TTS, key scenes converted and target-verified

**Steps**:
- [x] Run faster-whisper word timestamps over each scratch audio file in `manifest_pipeline/out/audio/*.wav`
- [x] Save per-section JSON under ignored `manifest_pipeline/out/alignments/`.
- [x] Add `narration_align.py` module: exact + fuzzy `find_phrase_time(section, phrase, occurrence=0) -> float | None`
- [x] Add `wait_until_phrase(phrase)` helper in base scene classes — compares against `self.renderer.time` and calls `breathing_wait(delta)`
- [x] Add strict overshoot mode via `RTV_STRICT_ALIGN=1`.
- [x] Add `check_phrase_anchors.py` preflight with alternate phrase support.
- [x] Add `anchor_phrases.json` for human-recording-safe anchor variants.
- [x] Document local human narration alignment workflow.
- [x] Convert key scenes S05, S07, S08/S06c, and S10 to phrase-anchored waits.
- [x] Convert S01, S02, and S03 to phrase-anchored waits.
- [x] Verify with targeted strict re-render + Gemini frame review.
- [x] Strict-render S01/S02/S03 after phrase anchoring; S03 was reshaped so early modality beats, tokenization, vectors, and late cards follow word-level anchors.
- [x] Re-render final S04/S06/S11 readability repairs locally with `RTV_VALIDATE_LAYOUT=1`.
- [ ] Gemini-review final S04/S06/S11 readability repairs after usage limit resets.

## Priority 3: Layout validation tests

**Goal**: Catch "text overflows box" / "element past safe area" / "two
visible elements overlap" before render.

**Status**: implemented helper layer, partially wired into scenes

**Steps**:
- [x] Add `layout_validate.py` module
- [x] Helper: `assert_text_fits(text_mobj, container_mobj)` — uses bounding boxes
- [x] Helper: `assert_in_safe_area(mobj, x_max=6.85, y_max=3.72)`
- [x] Helper: `assert_no_overlap(mobj_a, mobj_b)` — uses bounding box intersection with tolerance
- [x] Add opt-in `RTV_VALIDATE_LAYOUT=1` scene validation hooks.
- [x] Wire text-fit checks into `neon_box`, V-model nodes, tech-tree cards, and speculative rim cards.
- [ ] Add broader pairwise overlap report for selected named groups.

## Priority 4: Mermaid-first tech tree rework

**Goal**: Replace the misleading Signals/Control/Media row grid with a tech
tree whose layout reflects actual technical lineage.

**Status**: Deep Research-informed draft + deterministic layout parser implemented; S06c now includes a readable Mermaid-informed lineage beat before the workflow examples

**Steps**:
- [x] Write `drafts/tech_tree_lineage.mmd` — Mermaid graph showing real parent-child relationships
  - e.g. `Fourier --> frequency_space`, `embeddings --> speech_audio_agents`, `transformers --> code_agents`
- [x] Revise Mermaid draft from Deep Research output:
  - audio agents flow through neural codecs/discrete audio tokens, not Fourier/DCT;
  - SSMs are a convergence of control/state-space lineage with neural sequence modeling;
  - V&V systems converge from code agents, blackboard architectures, and formal verifiers.
- [ ] Get user review of the Mermaid graph before a full all-nodes visual replacement
- [x] Write `tech_tree_layout.py` that:
  - Parses the Mermaid graph
  - Handles Mermaid edge labels and dashed convergence edges
  - Computes node positions via a graph layout algorithm (e.g. graphviz-style hierarchy)
  - Returns a dict of `{node_id: (x, y, color, label)}`
- [x] Add Mermaid-informed lineage beat to `S06cGameTechTree3D`, replacing the row-grid reading at the key review frame with a readable critical-path tree.
- [ ] Full all-nodes `S06cGameTechTree3D` replacement from computed positions remains a future pass; the current version deliberately uses a readable subset because the full DAG is too dense for 480p.

## Constraints

- User wants ALL four done before next sync
- Hold the render until at least P2 (audio alignment) is in
- This file is the source of truth for progress — update after each step
- Save tokens by not reading PNG frames (use Gemini)
