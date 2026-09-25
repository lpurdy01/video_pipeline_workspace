# Editorial audience gate

## Purpose

The verification compiler answers whether a factual statement is traceable, scoped and consistently used. It is deliberately not a writing coach. Claim-level coverage is a poor proxy for reader value: it rewards retaining every qualification close to every claim and gives no credit for a concrete example, a clean causal explanation, or a useful decision takeaway.

This gate therefore evaluates a **complete reader artifact or section**, never an individual claim. It is advisory during drafting and becomes a separate human editorial acceptance before public release. It does not alter source-support, challenge, cross-artifact, human-disposition, or the assurance-case release calculation.

## Reader contract

Every paper section and video episode must be able to state, in one plain sentence:

1. the reader question it answers;
2. the concrete scene, decision, or artifact that makes the answer matter;
3. the mechanism or evidence that answers it;
4. the practical takeaway; and
5. the boundary that prevents overclaiming.

The preferred order is **scene → question → mechanism → takeaway → boundary**. A boundary belongs once at the end of the relevant thought unless its omission would make the preceding sentence false. It should not pre-empt every sentence with a disclaimer.

## Coverage goals

These metrics describe editorial completeness; they are not safety, accuracy, or release scores.

| Artifact | Coverage target | Human decision |
|---|---|---|
| Whitepaper | Every top-level section has a reader-contract row; each major concept is introduced through the road/air case or a manager-recognizable artifact before its taxonomy. | Editor accepts a section map and flags sections to cut, merge, or rewrite. |
| Video episode | One hook in the first 20 seconds, one question, one payoff visual, and one retained takeaway. | Editor accepts the beat map and runtime. |
| Cross-format | The paper may carry source detail; narration carries only the qualification needed for the spoken claim and points to the paper for the rest. | Editor checks that compression does not create an overclaim. |
| Claim tags | Tags remain machine-visible, but are clustered at the end of a paragraph or rendered as unobtrusive links in reader editions. | Editor checks that tags do not interrupt the sentence rhythm. |

A section fails this gate when it reads like a registry dump: a sequence of standards, claim IDs, caveats, or methods without a reader question and a decision-relevant conclusion. It also fails when it hides a material boundary merely to sound confident.

## Automated audience audit

`verification/gemini_nextgen_audit.py --task audience` is an **advisory artifact-level audit**. It asks a technical-generalist editor to identify the five highest-impact reader failures, not to verify sources. It must report: location; missing reader-contract element; exact reader confusion; a cut/merge/reorder/rewrite action; and whether a factual review is also needed. Model output is a lead, never a claim verdict, review record, source record, or human editorial acceptance.

Do not convert its result into a per-claim package or a percentage of safety/verification coverage. Keep a small editorial ledger of resolved high-impact findings instead. Human review should decide when the reader contract is satisfied.

## Immediate manuscript correction

The current whitepaper has grown to 9,675 words and is still organized around the evidence architecture. Before another research expansion, perform a reader-first restructure: start with the two-worlds encounter; explain the conventional playbook; show what ML breaks; then introduce the dated standards landscape, lifecycle, and methods only when the case needs them. Consolidate the eight contracts into one canonical presentation and move compiler-process detail to appendices. Do not use word count or negation count as a target to game; they are smoke alarms for a human edit.
