# Model or Tool Qualification

## Definition

Model or tool qualification is the practice of defining what a tool-like unit is allowed to do, how much confidence its output deserves, and what evidence is required before its output can be used in an assurance workflow.

For this project, model-unit qualification is inspired by tool qualification but should be described carefully: LLM agents are not DO-330 qualified tools merely because the project borrows the pattern.

## Why It Matters

The verification compiler delegates bounded verification tasks to model units. The project needs a way to express which tasks a model unit is qualified to perform, what review gates apply, and when independent challenge is required.

## Related Claims

- [Model Units Need Task-Specific Qualification](../claims/model_units_need_task_specific_qualification.md)

## Source Support

- Rierson explains that DO-330 was separated from the DO-178C core as a stand-alone tool qualification document, and that DO-178C section 12.2 determines whether and to what level a tool needs qualification. See Rierson Markdown line 5193.
- Rierson notes that tools with roles in both development and verification require consideration of independence between those functions. See Rierson Markdown line 21723.
- FAA AC 20-115D recognizes DO-330 and states that ED-12C/DO-178C section 12.2 and ED-215/DO-330 provide an acceptable method for tool qualification. See `faa_ac_20_115d.txt` line 540.
- NASA Jacklin explains that tool qualification depends on tool use, software level, and whether the tool generates or verifies software. See `nasa_ntrs_20120016835_jacklin_do178c.txt` line 278.

## Open Questions

- Should the whitepaper call the analogy "qualification-inspired" to avoid implying regulatory equivalence?
- What should a minimal model-unit qualification record contain?
