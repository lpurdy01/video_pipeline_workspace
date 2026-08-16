https://www.reddit.com/r/AI_Agents/comments/1sqg5ew/spent_a_weekend_actually_understanding_and/

https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code


https://www.analyticsvidhya.com/blog/2026/04/graphify-guide/

https://graphify.net/

## LLM capability and limits sources

- "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al., 2023): https://arxiv.org/abs/2307.03172
- "Context Length Alone Hurts LLM Performance Despite Perfect Retrieval" (Amazon/Du et al., 2025, EMNLP): https://arxiv.org/abs/2510.05381 [verify URL]
- Context rot analysis: https://research.trychroma.com/context-rot
- MMLU-Pro benchmark (TIGER-AI-Lab, NeurIPS 2024): https://arxiv.org/abs/2406.01574
- LLM bug detection task-specific accuracy (2025): https://arxiv.org/abs/2508.16419 [verify URL]

## Agent decomposition sources

- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., Google Brain, 2022): https://arxiv.org/abs/2201.11903
- "Modular Task Decomposition and Dynamic Collaboration in Multi-Agent Systems" (2025): https://arxiv.org/abs/2511.01149 [verify URL]
- "AgentOrchestra: A Hierarchical Multi-Agent Framework" (2025): https://arxiv.org/abs/2506.12508 [verify URL]
- "Towards Formal Verification of LLM-Generated Code from Natural Language Prompts" (2025): https://arxiv.org/abs/2507.13290 [verify URL]
- "VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation" (2025): https://arxiv.org/abs/2510.05156 [verify URL]

## Adaptability / model capability framing

- Dario Amodei interview (Dwarkesh Patel, 2025) — pre-training as evolution: https://www.dwarkesh.com/p/dario-amodei-2
- darioamodei.com: https://darioamodei.com/ (check for "Machines of Loving Grace" essay)

## Industry counterarguments / practitioner skepticism

- Beningo, Jacob. "Embedded software has 3 moats AI won't dissolve." LinkedIn, May 2026: https://www.linkedin.com/posts/jacobbeningo_embedded-software-has-3-moats-ai-wont-dissolve-share-7459936017232375808-ZCyu
  - NASA CAPSTONE embedded systems engineer; argues physics/certification/domain-expertise moats prevent AI from reaching safety-critical embedded software
  - Project response: moats are constraints on the *generator*, not the *verifier*; certification crosses via structured evidence production

## ISO 26262 (Automotive Functional Safety) — public proxy sources

- Volpe/U.S. DOT — Assessment of ISO 26262: https://www.volpe.dot.gov/sites/volpe.dot.gov/files/docs/Assessment%20of%20the%20ISO%2026262%20Standard,%20%E2%80%9CRoad%20Vehicles%20%E2%80%93%20Functional%20Safety%E2%80%9D.pdf
- NHTSA — Assessment of Safety Standards for Automotive Electronic Control Systems: https://www.nhtsa.gov/document/assessment-safety-standards-automotive-electronic-control-systems
- NHTSA DOT HS 812 574 (Hydraulic Braking): https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13497a_812574_hydraulicbrakingsystem.pdf
- NHTSA DOT HS 812 573 (Lane Centering): https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13498a_812_573_alcsystemreport.pdf
- NHTSA DOT HS 812 575 (Electric Power Steering): https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13501_812575_electricpowersteeringreport.pdf
- NHTSA DOT HS 812 576 (Steer-by-Wire): https://www.nhtsa.gov/sites/nhtsa.gov/files/documents/13502_812576_steerbywire.pdf

## IEC 62443 (Industrial/OT Cybersecurity) — public proxy sources

- CISA CPG 2.0 Report: https://www.cisa.gov/sites/default/files/2025-12/CPG_Report_2.0_508c.pdf
- CISA CPG 1.0.1: https://www.cisa.gov/sites/default/files/2023-03/CISA_CPG_REPORT_v1.0.1_FINAL.pdf
- CISA Cross-Sector CPG landing page: https://www.cisa.gov/cross-sector-cybersecurity-performance-goals
- NIST SP 800-82 Rev. 3 (OT Security Guide): https://csrc.nist.gov/pubs/sp/800/82/r3/final
- NIST SP 800-53 Rev. 5 (Security Controls): https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf
- ISA IEC 62443 Series Overview: https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- SANS Whitepaper (IEC 62443 overview): https://www.sans.org/white-papers/39960

## Captured public assurance sources

- FAA AC 20-115D: https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf
- NASA NTRS Jacklin DO-178C/DO-278A overview: https://ntrs.nasa.gov/api/citations/20120016835/downloads/20120016835.pdf
- NASA-STD-8739.8B: https://sma.nasa.gov/docs/default-source/policies/nasa-std-8739-8b.pdf
- NPR 7150.2D: https://nodis3.gsfc.nasa.gov/npg_img/N_PR_7150_002D_/N_PR_7150_002D_.pdf

## Public AS9100 references

- IAQG 9100 overview: https://iaqg.org/standard/9100-qms-requirements-for-aviation-space-and-defense-organizations/
- SAE AS9100D metadata: https://saemobilus.sae.org/standards/as9100d-quality-management-systems-requirements-aviation-space-defense-organizations
- NASA SMA AS9100/IA9100 article: https://sma.nasa.gov/news/articles/newsitem/2024/04/17/status-of-the-development-of-ia9100-quality-management-systems-requirements-for-aviation-space-and-defense-organizations
