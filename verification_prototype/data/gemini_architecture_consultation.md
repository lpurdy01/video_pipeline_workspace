# Gemini 3.1 Pro (High Thinking) — Architecture Consultation

Generated: 2026-05-19
Model: gemini-3.1-pro-preview (thinking_level=HIGH)

---

This is an exceptional set of findings. Self-applying a system to its own specification is a classic "dogfooding" technique, and the artifacts you've provided show exactly why it's valuable. The failures are not merely bugs; they are architectural omissions.

Here is my analysis of the three discoveries, followed by the synthesized schema, formula, and strategic decisions you requested.

---

### ANALYSIS OF DISCOVERIES

#### DISCOVERY 1: Source citations need stable, retrievable region pointers

Code units have ASTs (Abstract Syntax Trees); documents do not. Relying on natural-language keyword matching for source resolution is a foundational error in the builder because it breaks the "provable decomposition" property. If the graph cannot deterministically map a requirement to the exact text it references, you cannot assemble a context-window-bounded Verification Query Package (VQP).

*   **Properties of a stable source ID:**
    1.  *Immutable:* The target text must not change without the ID (or its hash) changing.
    2.  *Granular:* It must point to a strictly bounded region (e.g., a paragraph or table), not just a whole document, to prevent blowing out the LLM context window.
    3.  *Dereferenceable:* The builder pipeline must be able to resolve the ID to a raw text string programmatically.
    4.  *Machine-readable:* It must rely on a standard schema, not heuristics.
*   **Minimum Viable Addressing Scheme:**
    *   **(a) Academic papers:** `doi:<number>#page=<n>&bbox=[x1,y1,x2,y2]` or (speculation) if converted to markdown, `arxiv:<id>#sec:<slug>`.
    *   **(b) Engineering standards (DO-178C):** Hierarchical index locators. `std:DO-178C:2011#table:A-1:obj:3` or `std:DO-178C:2011#para:6.3.1`.
    *   **(c) Internal documents:** Git URI with line anchors or markdown headers. `git-blob:<hash>:<path>#H3:<header-slug>` or `...#L<start>-L<end>`.
*   **Artifact Graph Edge:** The edge must be `supports-claim` pointing from a `RequirementNode` to a `SourceRegionNode`. The edge itself should contain `extraction_selector` metadata (e.g., an XPath or line range).
*   **Retrieval Mechanics:** At VQP assembly time, a "Resolver" component reads the `SourceRegionNode`. It hits an internal Document Server or object store, pulls the document matching the version hash, applies the selector (e.g., parsing the Markdown for an H3 boundary), and directly injects the raw string payload into the prompt context.

#### DISCOVERY 2: Coverage has two dimensions the current VRM conflates

Collapsing horizontal coverage (scope) and vertical coverage (evidence completeness) hides critical system state. A node with missing evidence and a node with evaluated-and-failed evidence are fundamentally different: the former is a *process* failure; the latter is a *software* failure.

*   **Separating Horizontal and Vertical:**
    *   *Horizontal Coverage ($C_h$)* is boolean scoping: what percentage of in-scope code units have a completed VQP?
    *   *Vertical Coverage ($C_v$)* is evidence depth per VQP: of the required artifact edges (req, test, code, static analysis), what percentage exist and are valid?
*   **Per-Node Evidence Completeness Model:** It should be a *weighted fractional* model. Critical evidence types (e.g., "Has Requirement", "Has Test") are mandatory; if missing, vertical coverage for that node is 0. Supplementary evidence (e.g., "Has Static Analysis") provides fractional boosts.
*   **Version Consistency (Staleness):** Evidence tied to older code versions shouldn't be binary rejected unless it's a structural mismatch. Instead, it applies a *Staleness Discount* ($S \in [0, 1]$). A test result from the current commit is 1.0; a result from a week ago is 0.8; if the AST of the target function changed, it is strictly 0.0.
*   **Distinguishing States:**
    *   *Missing evidence:* Lowers the Vertical Coverage ($C_v$).
    *   *Evaluated & Passed:* Contributes positively to the Verdict Confidence ($V$).
    *   *Evaluated & Failed:* Drops the Verdict Confidence ($V$) to near-zero (the codebase is explicitly *not* ready).

#### DISCOVERY 3: Model confidence needs empirical calibration, not self-reporting

The prototype proved what the literature states: LLMs are poor at estimating their own epistemic uncertainty. Gemini returning 1.0 confidence on an objectively failed citation mapping is expected behavior. The asymmetry highlighted in arXiv:2603.00539 (FPR > FNR) means we must use Bayesian calibration.

*   **Accuracy Profile Architecture:**
    *   We need a `ModelAccuracyProfile` database/node mapped by `(Model_ID, Prompt_Version, Task_Type)`.
    *   Fields: `True_Positives`, `False_Positives`, `True_Negatives`, `False_Negatives`, `Sample_Size`, `Last_Updated`.
    *   *Initialization:* Pessimistic prior using Laplace smoothing (e.g., Beta distribution initialized as if the model has a 50/50 coin-flip record until proven otherwise).
*   **Incorporating Directional Error:**
    *   If the model says "PASS", the true probability of compliance is the Positive Predictive Value ($PPV$).
    *   If the model says "FAIL", the true probability of compliance is $1 - NPV$.
    *   VRM uses these calibrated probabilities instead of the raw LLM output. Because LLMs overcorrect (high FPR), a "FAIL" verdict will reflect a moderate penalty, but a "PASS" verdict (given low FNR) provides extremely high confidence.
*   **Canary Queries:** To continuously update the profile without waiting for human review, the CI pipeline must blindly inject *known-good* (historical accepted code) and *known-bad* (mutated code with seeded bugs) queries. The LLM evaluates these, and the system silently updates the FPR/FNR counters in the `ModelAccuracyProfile`.
*   **The Bootstrap Problem:** On Day 1, with no profiles, the VRM will naturally be low because of the pessimistic Bayesian prior. The fastest way to bootstrap is to run the model against a historical archive of the team's past PRs (where the human verdict is known) to pre-seed the $TP/FP/TN/FN$ matrix.

---

### SYNTHESIS REQUEST

#### 1. Updated Core Schema

To address the discoveries, the Artifact Graph schema requires the following additions:

**New Nodes:**
*   `SourceRegionNode`: Represents a bounded segment of text. Primary Key: `URI_Locator` (e.g., `doi:10.xxx#sec:3`). Attributes: `Content_Hash`, `Text_Payload`.
*   `ModelAccuracyProfile`: Represents the empirical performance of an agent. Primary Key: `[Model_ID, Prompt_Version, Task_Type]`. Attributes: `TP, FP, TN, FN, Prior_Alpha, Prior_Beta`.

**Modified Edges:**
*   `traces-to` and `verified-by`: Must now include `Source_Version_Hash` and `Target_Version_Hash` to calculate the Staleness Discount.
*   `supports-claim`: New edge connecting a `RequirementNode` to a `SourceRegionNode`, containing `Selector_Logic` (how to extract the specific claim from the region).

#### 2. A Better VRM Formula

The VRM must combine Horizontal Coverage ($C_h$), Vertical Coverage ($C_v$), Staleness ($S$), and Empirically Calibrated Verdicts ($V$).

Let $N_{total}$ be the total number of code units in scope.
Let $N_{eval}$ be the subset of code units that have undergone a VQP evaluation.

**Horizontal Coverage:**
$$C_h = \frac{|N_{eval}|}{|N_{total}|}$$

**Vertical Evidence Completeness (for query $i$):**
$$C_v(i) = \sum_{k \in \text{EvidenceTypes}} w_k \cdot I_k \cdot S_k$$
Where $w_k$ is the weight of the evidence type (sum of $w_k = 1$), $I_k$ is a binary indicator of existence, and $S_k \in [0,1]$ is the version staleness discount.

**Calibrated Verdict Score (for query $i$):**
We discard the LLM's self-reported float. Based on the model's profile for the specific task, we calculate Bayesian predictive values:
*   If LLM outputs PASS: $V(i) = PPV = \frac{TP}{TP + FP}$
*   If LLM outputs FAIL: $V(i) = 1 - NPV = 1 - \frac{TN}{TN + FN}$
*(Note: These should be smoothed using Bayesian priors to prevent 1.0/0.0 extremes on low sample sizes).*

**Final VRM Formula:**
$$VRM = C_h \times \left( \frac{1}{|N_{eval}|} \sum_{i \in N_{eval}} C_v(i) \times V(i) \right)$$

*Meaning:* The VRM is the percentage of the system we've looked at ($C_h$), scaled by how complete the evidence is ($C_v$) and the empirical likelihood that the code is actually compliant based on the LLM's historical accuracy ($V$).

#### 3. The 3 Most Important Unresolved Architectural Decisions

Before Stage 2 implementation, you must resolve these issues not covered in the requirements:

1.  **The Graph Invalidation Cascade:** When a developer commits a change to a single C function, how much of the graph is invalidated? Does a change to a parent requirement invalidate all child code VQPs? You must define the trigger logic for re-evaluating nodes, or the CI system will waste immense compute traversing unaffected sub-graphs.
2.  **Handling Multi-Unit / Emergent Requirements:** The requirements document assumes a `requirement -> code unit` trace. How does the compiler handle a requirement that dictates system timing or memory budgets spanning 50 functions? Bounding this into a single context window is impossible. You must decide whether to support "System-Level VQPs" (relying on static analysis summary nodes rather than raw code) or restrict the VC strictly to unit-level properties.
3.  **Conflict Resolution Economics:** Under REQ-3-4, human results override LLM results and trigger a profile update. If a human override alters the $FPR$ for a model, the calibrated confidence $V(i)$ for *all historical queries* evaluated by that model shifts. Does the system retroactively update the global VRM? Does it trigger re-evaluation? You must define the lifecycle of historical evidence when the empirical lens observing it changes.

#### 4. What the Prototype Revealed about Code vs. Documents

Applying the VC to the whitepaper revealed a profound insight: **The Verification Compiler relies fundamentally on the strict boundaries of programming languages; natural language resists decomposition.**

Code verification via AST parsing provides absolute, deterministic boundaries. Function A begins at line 10 and ends at line 45. Scope is unarguable. The prototype revealed that prose has "bleeding context." A requirement might span a section header, three paragraphs, and an implicit reference to an earlier diagram. When the prototype truncated text at 4,000 characters, it broke the semantic meaning of the document. Truncating an AST node simply invalidates the JSON.

**What this tells us about the design:**
If you ever intend to apply the VC to systems engineering artifacts (SysML, textual requirements documents, ICDs), *you cannot treat them as raw text.* To be verifiable by this architecture, documents must be authored using structural constraints akin to code (e.g., Markdown headers as strict scopes, atomic sentence claims mapped to anchors). The VC concept does not solve NLP ambiguity; it simply exposes it. For Stage 2 (C code), this validates the choice to rely heavily on ASTs and static analysis tools as the primitive node boundaries.