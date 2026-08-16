# Rierson DO-178C Source Note

## Provenance

raw_file: refrence_literature/Developing_safety_critical_software/Rierson, Leanna - Developing Safety-Critical Software _ A Practical Guide for Aviation Software and DO-178C Compliance (2013, CRC Press).md
raw_url: null
summary_method: llm-extract-from-raw
summary_verified: false

## Source

Leanna Rierson, `Developing Safety-Critical Software: A Practical Guide for Aviation Software and DO-178C Compliance`, extracted Markdown at:

`refrence_literature/Developing_safety_critical_software/Rierson, Leanna - Developing Safety-Critical Software _ A Practical Guide for Aviation Software and DO-178C Compliance (2013, CRC Press).md`

## Why It Matters

This source grounds the whitepaper's safety-critical engineering side. It provides support for claims about verification, review, traceability, tool qualification, independence, and evidence-producing process structure.

## Key Ideas

- DO-178C verification is an integral process spanning plans through reported verification results, and includes reviews, analyses, and tests.
- Traceability should be documented while requirements are written, because reconstructing traces later is described as practically infeasible.
- Requirements reviews check not only content quality but also traceability from high-level software requirements to system requirements.
- Software verification planning records how reviews, analyses, tests, traceability, pass/fail criteria, and results will be handled.
- DO-330 provides a separate software-tool qualification framework, with qualification rigor tied to tool usage and tool qualification level.

**Critical citation — DO-178C independence definition (Section 9.3, p. 188; Rierson markdown lines 12056–12059):**

> "Separation of responsibilities which ensures the accomplishment of objective evaluation. (1) For software verification process activities, independence is achieved when the verification activity is performed by a **person(s)** other than the developer of the item being verified, and **a tool(s) may be used to achieve equivalence to the human verification activity.**"

Rierson commentary immediately follows (lines 12112–12114): "the verification is only as good as the person or tool doing the verifying. Therefore, it is important to use skilled personnel or effective tools. In some cases the tools may need to be qualified (see Chapter 13)."

**Independence by DAL (lines 12069–12079):**
- DAL A: 25 verification objectives require independence
- DAL B: 13 verification objectives require independence
- DAL C/D: no verification objectives require independence
- Tables A-3 through A-5 independence: typically satisfied by a separate person reviewing data they did not write
- Table A-6 independence: satisfied by having someone who did not write the code write the tests

**Human reviewer qualification (lines 3655–3656, Section 3.3.3):**

> "DO-178C assumes the use of qualified and well-trained people; however, it is difficult to measure the adequacy of people. Some authorities examine resumés and training history to ensure that qualified and properly trained personnel are used."

This is informally defined — no formal certification is required for human reviewers. Qualification is assessed via résumés and training history.

**Peer review guidance (lines 8703–8710):**
"Use qualified reviewers. Key technical reviewers include those who will use the data (e.g., tester and designer) and one or more independent developers (when independence is required)... The review will only be as good as the people performing it."

## Useful Claims

- Safety-critical verification is not only testing; it includes review, analysis, and test activities that produce reviewable evidence.
- Safety-critical requirements work depends on bidirectional traceability among system requirements, high-level software requirements, low-level requirements, test data, and verification results.
- Traceability is cheaper and more reliable when built during requirements development instead of reconstructed after the fact.
- Tool or model units used in verification-like roles need task-specific qualification, usage boundaries, and evidence about their operational role.
- **DO-178C independence can be satisfied by person(s) OR by a qualified tool.** The standard's exact definition includes both: "a tool(s) may be used to achieve equivalence to the human verification activity." Tool equivalence requires DO-330 qualification. This is the architectural pathway for the Verification Compiler.
- Human reviewer "qualification" is informally assessed (résumés, training history). DO-330 tool qualification is more formal and rigorous — an interesting asymmetry.

## Requirements Impact

- A verification compiler should create trace links as requirements are decomposed, not as an after-the-fact cleanup step.
- Each trace link should have a stable ID, source evidence, relation type, status, and review history.
- Review tasks should produce evidence artifacts, not just pass/fail answers.
- Tools or model units used by the compiler should have explicit qualification records tied to their delegated task types.

## Follow-Up Questions

- Which DO-178C traceability objectives should be modeled directly in the Stage 2 prototype?
- Should model-unit qualification be framed by analogy to DO-330, or kept as a looser "qualification-inspired" design pattern?
- What source span format should the project use for extracted books where page numbers are imperfect but Markdown line numbers are stable?
