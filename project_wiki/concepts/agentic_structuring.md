# Agentic Structuring

## Definition

Agentic structuring is the practice of organizing systems of units of intelligence — humans, models, tools — into hierarchies, delegation patterns, and review loops that allow the system to accomplish more reliable work than any individual unit could accomplish alone.

The concept applies both to human organizations (companies, engineering teams, certification bodies) and to systems of AI agents. The structural principles are similar because the underlying problem is the same: coordinating limited-capacity, imperfectly-accurate units into collective work of acceptable quality.

## Why Structure Matters

A single general-purpose unit faces compounding limits:

- Its capacity is finite — it cannot hold the entire problem in view at once
- Its accuracy degrades on tasks outside its specialization
- Its outputs are harder to review when the reasoning is opaque or spans too many concerns at once
- Its failures propagate without a review layer to catch them

Decomposing work into bounded tasks and assigning them to specialized units addresses each of these limits. Hierarchy and delegation are the organizational mechanisms for doing this at scale.

This is not a novel idea. Human organizations have used it for as long as complex work has existed. Safety-critical engineering standards encode it explicitly: DO-178C requires independence between verification and development roles; AS9100 structures quality oversight as a separate organizational function; NASA directives require independent verification and validation for high-criticality software.

## Organization Shape as a Design Variable

The shape of the hierarchy matters. Different kinds of work call for different structures:

**Verification-heavy structures** tend toward lower span of control (fewer direct reports per manager), because the manager's role involves reviewing and approving the work of subordinates. The bottleneck is the manager's review capacity, so spans are kept narrow to preserve review quality.

**Innovation-oriented structures** tend toward wider span of control (many direct reports per manager), because the manager's role is coordination and enablement rather than detailed review. Each subordinate is a high-specialization unit operating more autonomously.

This intuition comes from observing the contrast between organizations like traditional aerospace engineering programs (narrow spans, deep review hierarchies) and technology companies optimized for fast iteration (flat structures, autonomous teams). Nvidia is a notable example of the latter — reportedly among the widest management spans in the industry — and has been unusually productive relative to headcount.

*(Citation target: reporting on Nvidia organizational structure; organizational theory on span of control and hierarchy shape.)*

## Relationship to the Verification Compiler

The verification compiler is an instance of agentic structuring applied to verification work specifically:

- The hierarchical requirements graph is the decomposition structure
- Graph traversal is the delegation mechanism — work is assigned to units (models or humans) based on what fits in their context window
- Independent review mode (human replacing LLM or vice versa) is the independence requirement, analogous to DO-178C's independent verification requirement
- The confidence score is the aggregate quality signal from the decomposed work, analogous to a review board's judgment about whether individual review records constitute sufficient assurance

The structure of the verification compiler is verification-heavy: each unit of work (one verification query) is bounded and reviewed independently. The graph structure is the mechanism that makes this manageable without requiring any unit to hold the entire system in view.

## Distinction from Multi-Agent Optimization

The organizational analogy (hierarchy improving intellectual work, Nvidia management span, etc.) is conceptual background for the whitepaper's motivation. The verification compiler itself is not a multi-agent system in the sense of autonomous agents collaborating dynamically. It is a structured, deterministic decomposition that happens to use LLMs as reviewers for bounded work packets.

The relevant claim is simpler: decomposing large verification problems into bounded, well-defined units improves the reliability of the overall verification result, regardless of whether the reviewers are humans or models. This claim is supported by the existence of mature safety-critical standards that mandate exactly this decomposition pattern.

## Open Questions

- At what span of control does a model-as-manager pattern become useful in verification workflows (e.g., a coordinating agent that routes queries to specialist models)?
- Is there a useful distinction between "orchestration" (routing and assembling work) and "verification" (judging correctness) that should be reflected in the compiler architecture?
- What is the right analogy for the verification compiler's graph traversal in organizational terms — a project plan, a review board schedule, something else?
