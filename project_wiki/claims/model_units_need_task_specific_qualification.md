# Model Units Need Task-Specific Qualification

## Claim

Model or agent units used in verification workflows need task-specific qualification, usage boundaries, and review gates before their outputs can support safety-critical evidence.

## Status

Speculative project claim with analogy support from Rierson's discussion of DO-330. Needs AI assurance and LLM evaluation sources.

## Supporting Sources

- Rierson: DO-330 explains whether a tool needs qualification and to what level, and provides a stand-alone framework for qualifying software tools. Evidence location: Rierson Markdown line 5193.
- Rierson: tools that have roles in both development and verification require consideration of independence between those roles. Evidence location: Rierson Markdown line 21723.
- [FAA AC 20-115D](../sources/faa_ac_20_115d.md): section 12.2 of ED-12C/DO-178C and ED-215/DO-330 provide an acceptable method for tool qualification, with objectives, activities, and life cycle data. Evidence location: `faa_ac_20_115d.txt` line 540.
- [NASA Jacklin DO-178C and DO-278A](../sources/nasa_jacklin_do178c_do278a.md): tool qualification depends on tool use, software level, and whether the tool generates or verifies software. Evidence location: `nasa_ntrs_20120016835_jacklin_do178c.txt` line 278.

## Challenges or Uncertainty

- LLM agents are not equivalent to DO-330 tools. The whitepaper should frame this as a qualification-inspired coordination pattern, not as a claim that model units can directly satisfy DO-330.
- Still needs sources on LLM evaluation, AI assurance, model governance, and tool-use reliability.

## Whitepaper Use

Use in Stage 1 sections:

- `5. Qualification of Model Units`
- `6. Verification Compiler Concept`
- `7. Requirements for the Stage 2 Prototype`
