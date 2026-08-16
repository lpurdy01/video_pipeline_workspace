# Introductory Composition

## Working Title

Agentic Structuring for Verification and Validation in Safety-Critical Software Engineering

## Project Goal

The goal of this project is to research agentic structuring so that we can improve the use of agents in safety-critical software engineering.

In safety-critical software, a large amount of human time is spent in the verification stage. In this workspace, we are working toward a verification-validation pipeline that can allow software development to be verified against its specification while minimizing human interaction with tedious tasks.

The system should preserve the parts of safety-critical engineering that require human judgment while reducing the burden of repetitive checking, traceability maintenance, review preparation, consistency analysis, and evidence organization.

## Motivation

Safety-critical software engineering requires extensive verification, validation, documentation, traceability, review, and compliance work. These activities are necessary because failures can have severe consequences, but many parts of the workflow are meticulous rather than creatively difficult.

This project begins from the observation that modern agent systems may be useful in this setting if they are structured correctly. A single agent is limited by its context window, reliability profile, specialization, and task framing. A structured system of agents may be able to perform more useful work by dividing responsibilities, specializing behavior, and creating review loops between separate units of intelligence.

## English as a Specification Medium

English is an imprecise medium for specifying software interactions. It is interesting that safety-critical engineering often depends on the concept of an English-language specification at all.

Natural-language specifications can be useful because they are accessible to humans, certifiers, customers, and engineering teams. However, they also create problems:

- specifications may be ambiguous
- important assumptions may remain implicit
- implementation may drift from intent
- verification evidence may be incomplete
- reviewers may interpret requirements differently
- compliance artifacts may become disconnected from engineering work

An important research question is whether agentic systems can help translate between natural-language specifications, formal or semi-formal expectations, implementation artifacts, tests, and verification evidence.

## Core Concept: Units of Intelligence

The initial idea for this project comes from thinking about agents, humans, and teams as units of intelligence.

A unit of intelligence has several relevant properties:

- **Capacity:** roughly analogous to short-term memory, context window size, and the amount of information that can be considered at once.
- **Accuracy:** the degree to which the unit produces correct judgments or outputs. Accuracy may have several forms and may be a function of the available context window, task type, prompting, review structure, and feedback.
- **Adaptability:** the ability to adjust behavior in response to new information, examples, corrections, and environmental constraints.
- **Specialization:** the degree to which the unit is optimized for a particular class of tasks.
- **Reviewability:** the degree to which the unit's work can be inspected, challenged, reproduced, or validated by another unit.
- **Qualification:** the degree to which the unit has been validated as capable of performing a delegated task.

Adaptability seems to come in layers. One useful analogy is that building a foundation model may be more like recreating many components of human brain evolution than like a single human brain adapting. Humans come with many prebuilt structures, so the rate at which a human can adapt and learn is much faster in some settings. This may connect to Dario Amodei or Anthropic writing and should be supported with a citation later.

This framing applies both to humans and to machine agents. Humans have long developed organizational structures that allow limited individual intelligence to accomplish larger goals through collaboration. Agent systems may need comparable structures.

## Agentic Structuring Hypothesis

Recent agentic development practice suggests that, because the capacity of individual units of intelligence is limited, subdividing tasks and specializing roles is a useful way to let systems of units accomplish more than they could individually.

This resembles hierarchy and specialization in human organizations. Companies, engineering teams, certification bodies, review boards, and quality organizations are all shaped around the problem of coordinating limited human capacity into reliable collective work.

The structure matters. Depending on the kind of work a company or project is trying to accomplish, it may shape its organization very differently.

One hypothesis is that more innovative organizations often have flatter structures, while still preserving high specialization. In those organizations, a manager may have 20 or more direct reports, and the work is collaborative between units of intelligence, with each person bringing a unit of experience and specialization.

In more task-oriented or managerial structures, the number of direct reports may be much lower because the manager's role is more involved in verification of correctness than in enabling innovation.

This intuition comes from learning about Nvidia's organizational structure and relating it to professional engineering organizations, especially the question of how many direct reports different kinds of managers may have.

The research question is therefore not simply:

> Can an agent do verification?

A better question is:

> What agentic structures can support reliable verification and validation workflows for safety-critical software?

## Safety-Critical Engineering as a Collaboration System

Humans have been working together as units of intelligence for a long time, and we have developed many collaboration systems that allow us to specialize and accomplish tasks effectively.

One category of collaboration systems is the set of concepts necessary for safety-critical software development, or safety-critical engineering in general.

Important recurring components include:

- **Verification and validation:** checking that work products satisfy specified requirements and that the resulting system satisfies the intended operational need.
- **Feedback:** using defects, review findings, test outcomes, and operational evidence to improve the system.
- **Review:** independent or semi-independent examination of artifacts, assumptions, decisions, and evidence.
- **Traceability:** maintaining explicit relationships between requirements, design, implementation, tests, hazards, and verification evidence.
- **Configuration control:** ensuring that changes are deliberate, reviewed, and recoverable.
- **Process assurance:** checking that the development and verification process itself is being followed.
- **Issue tracking:** ensuring that errors and updates are recorded so the next version of the work does not carry known issues forward.

There are common organizational and project patterns, with shared components across:

- AS9100
- Design Assurance Level certification concepts
- DO-178C-based software development
- NASA software engineering and safety directives

Most of these methods theorize ways to conduct work as units of intelligence within a system so that the work reaches a standard useful to the larger system. These methods are designed to construct safe products. The work produced must do what is expected of it without side effects. Errors, updates, and known issues must be tracked. Boards, reporting structures, reviews, and other process elements are used to maintain organizational quality.

## Measurement and Qualification of Units of Intelligence

In order for engineers to be allowed to work on safety-critical software, they must be qualified for the work. Organizations establish their own methods for this. These qualification processes may not directly create safe software, but they remain critical to the process of constructing confidence in the work.

Often candidates are required to have an accredited education that comprises many layers of tests and educational standards reviewed by boards. After that, there is usually an interview process or other validation process before engineers join teams.

Models and systems of models will also need to be verified in some way to ensure that delegated work is within their qualifications.

Possible questions:

- How do we qualify a model for a specific verification task?
- Can a model be qualified for one task but not another?
- What evidence is needed before work can be delegated to a model?
- How should a system track which model, prompt, context, and toolchain produced a given result?
- What review process is needed before model-generated verification evidence can be trusted?

## Concept: Validation Compiler

The concept of a validation compiler is to create a system that, given access to sufficiently qualified LLMs for each unit task through an API or similar mechanism, can atomically break down requirements in a requirements traceability tree, as standards like DO-178 describe, and validate the implementation against those requirements.

This is a compiler for DO-178-style validation work. It is not a literal software compiler. Instead, it targets the normally human task of validating that implemented code meets the specification described.

The validation compiler would transform a collection of requirements, implementation artifacts, and verification evidence into structured claims about whether the implementation satisfies the specification.

## Possible Verification-Validation Pipeline

A possible pipeline might include:

1. **Specification intake:** collect requirements, assumptions, definitions, constraints, and acceptance criteria.
2. **Specification structuring:** transform natural-language requirements into structured claims, interfaces, behaviors, invariants, and traceable units.
3. **Requirement decomposition:** break large requirements into atomic units that can be individually checked.
4. **Traceability tree construction:** connect high-level requirements, low-level requirements, design artifacts, source code, tests, and verification evidence.
5. **Implementation analysis:** inspect source code, configuration, tests, and design artifacts.
6. **Consistency checking:** identify ambiguity, missing links, conflicts, under-specified behavior, unsupported claims, and possible side effects.
7. **Verification planning:** propose test cases, review checks, static analysis targets, or formalization opportunities.
8. **Delegated agent work:** assign bounded verification tasks to qualified model units.
9. **Independent review:** use separate agents or humans to challenge assumptions and inspect evidence.
10. **Evidence packaging:** produce artifacts that support human review, certification reasoning, or model ingestion.

## Research Questions

- What kinds of safety-critical verification work are suitable for agent assistance?
- Which tasks should remain human-led, and which can be delegated to agents?
- What agent role structure best supports verification, validation, review, and traceability?
- How should agents handle ambiguous English-language requirements?
- How can an agentic system expose uncertainty instead of hiding it?
- How can outputs be made auditable enough for safety-critical engineering?
- What evidence should an agent produce when it claims that software satisfies a specification?
- Can safety standards be used as templates for agent organization?
- How should context be partitioned so that agents can reason over large systems without losing important details?
- How should models be qualified for specific delegated tasks?
- What does it mean for a system of models to be qualified?
- Can organizational patterns from innovative companies and safety-critical companies inform different agent hierarchy shapes?

## Expansion Areas

### English as a Specification Medium

Expand on why English is useful but imprecise for software specification. Discuss ambiguity, underspecification, domain assumptions, implicit knowledge, and the difficulty of translating natural language into executable or verifiable behavior.

Possible expansion:

- examples of ambiguous requirements
- distinction between user intent, system requirements, software requirements, and tests
- relationship between natural language, formal methods, and semi-formal representations

### Units of Intelligence

Expand the theory of units of intelligence. Compare humans, individual language model agents, specialized tools, review boards, organizations, and model systems.

Possible expansion:

- capacity limits and context windows
- accuracy as task-dependent rather than global
- specialization versus generality
- adaptability in humans compared with foundation models
- qualification and evidence of competence
- citation target: Dario Amodei or Anthropic writing on model capabilities, adaptation, and intelligence

### Hierarchies and Agent Organizations

Expand the analogy between companies and agent systems. Discuss why hierarchy, specialization, delegation, and review exist in human organizations.

Possible expansion:

- flatter structures in innovative organizations
- lower direct-report structures in verification-heavy organizations
- Nvidia as a possible case study or intuition source
- when hierarchy improves reliability
- when hierarchy creates communication failures
- agent manager/reviewer/worker patterns
- independent verification and validation as an organizational pattern

### Safety-Critical Process Patterns

Expand the comparison between safety-critical standards and agentic workflows.

Possible expansion:

- DO-178C objectives and evidence structures
- requirements traceability trees
- Design Assurance Levels and rigor scaling
- NASA software assurance patterns
- AS9100 quality management concepts
- process assurance as a model for agent oversight
- boards, reviews, reporting structures, and issue tracking

### Measurement and Qualification

Expand the idea that humans must be qualified before working on safety-critical software, then ask how a comparable process might apply to models and agent systems.

Possible expansion:

- accredited education and professional qualification analogies
- model evaluation for delegated work
- task-specific model qualification
- prompt and context qualification
- reproducibility and audit logs
- independent challenge by another model or human

### Validation Compiler

Develop the validation compiler concept into a concrete architecture.

Possible expansion:

- input artifact types
- output artifact types
- requirement atomization
- traceability schema
- agent role definitions
- human review gates
- model-ingestion format
- evaluation benchmarks

### Evaluation and Trust

Define how we would know whether the system is useful.

Possible expansion:

- defect discovery rate
- false positive and false negative rates
- traceability completeness
- review time reduction
- reproducibility of agent judgments
- auditability of outputs
- human confidence and calibration

## Citation Targets

- Research on agent decomposition, multi-agent collaboration, and specialization.
- Work on context window limitations and long-context reliability.
- Dario Amodei or Anthropic writing on AI capability, adaptation, and model behavior.
- Evidence on Nvidia organizational structure and management span.
- Organizational theory about hierarchy, specialization, innovation, and verification-oriented management.
- DO-178C and related aviation software certification material.
- NASA software engineering and software assurance directives.
- AS9100 or aerospace quality management references.
- Literature on formal methods, requirements ambiguity, and natural-language specification.
- Literature on engineer qualification, process assurance, and certification evidence.

## Draft Thesis

Safety-critical software engineering can be understood as a disciplined collaboration system for limited units of intelligence. Modern agent systems introduce new units of intelligence with different strengths and failure modes. If these units are structured and qualified according to principles drawn from safety-critical engineering itself, they may become useful participants in verification and validation workflows, especially for traceability, consistency checking, review preparation, and evidence organization.

The long-term idea is a validation compiler: a system that decomposes requirements into traceable units, delegates bounded verification tasks to qualified model units, validates implementation artifacts against those requirements, and packages the resulting evidence for human review.
