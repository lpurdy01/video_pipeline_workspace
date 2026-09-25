"""Run an isolated, search-grounded Gemini source-discovery and challenge pass.

The response is deliberately kept under ignored out/.  It is a lead list, never
source context or an accepted project claim.  The integrator must independently
retrieve and inspect every candidate before creating a source record.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
WORKSPACE = PROJECT.parent
SPACE = Path(__file__).resolve().parent
OUT = SPACE / "out"

sys.path.insert(0, str(WORKSPACE))
from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402


def read(relative: str, limit: int = 14000) -> str:
    text = (PROJECT / relative).read_text(encoding="utf-8")
    return text[:limit] + ("\n[truncated for research prompt]" if len(text) > limit else "")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    packet = {
        "project_brief": read("PROJECT_BRIEF.md"),
        "decisions": read("planning/decisions.md"),
        "next_steps": read("planning/learned_systems_assurance_next_steps.md"),
        "research_questions": read("research/questions.md"),
        "architecture": read("assurance/architecture.md"),
        "whitepaper_outline": read("resource_composition/whitepaper_outline.md"),
        "retrieval_status": read("research/retrieval_status.md"),
        "round2_integration": read("research/integration_round2.md"),
    }
    prompt = """You are an independent research scout with Google Search grounding for a
public whitepaper/video project: Assurance for Learned Autonomous Systems.

Your role is discovery and adversarial challenge. Do not write the paper and do
not imply that a source proves certification of any proprietary vehicle.

The target is a FROZEN, VERSIONED TRAINED model used in a bounded
safety-critical autonomous role. Models that learn during operation are a
separate, harder comparison. The project seeks a practical assurance case: ODD
and authority; data/training/release lineage; scenario/statistical evidence;
uncertainty and ODD exit; closed-loop dynamics; monitor/recovery; change
control; and claim-specific formal or interpretability analysis.

Search for high-value, publicly citable sources NOT already covered by the
project packet. Prioritize primary authorities, standards bodies, peer-reviewed
papers with stable URLs, NTSB/NHTSA/FAA/EASA/CAA material, and public assurance
cases. Seek especially:
1. A public end-to-end assurance lifecycle or accepted means that could defeat
   the project's tentative 'partial toolkit' framing.
2. Concrete evidence on rare-event statistics, scenario coverage, dataset
   representativeness, uncertainty/calibration, model release/change control,
   runtime assurance, neural-network verification, interpretability and
   evidence composition.
3. Aviation learned/perception/DAA safety assurance beyond generic AI roadmaps.
4. Road-vehicle learned-system assurance beyond Tesla news.
5. Citable visual media: official diagrams, public figures, presentations,
   animations or videos whose license/status and claim can be checked. A visual
   is only useful if a public resource package can link to it lawfully.
6. The current division of responsibility between regulators, standards bodies,
   manufacturers and independent assessors for trained components. Test the
   claim that automotive manufacturers may self-certify carefully: identify
   the jurisdiction, statutory mechanism, and limits rather than generalizing
   it into an assurance conclusion.
7. Current DAL/design-assurance concepts and any published AI-criticality or
   autonomy boundaries. Separate an authority's discussion or research roadmap
   from binding accepted certification guidance.
8. Evidence that separates a statistical model-evaluation tradeoff (for
   example sensitivity, false-alarm rate, calibration, confusion matrix) from
   a system safety argument about hazardous outcomes and recovery.

Avoid duplicate leads already covered in the packet: FAA AI Roadmap v1; EASA
Issue 2 and Proposed Issue 3; ISO/PAS 8800 and ISO 21448 public records; UL
4600 overview; NASA runtime-assurance/UAS papers; UK CAA CAP3127; FAA DAA TSO
and exemption material; GA-ASI reports; Texas authorization pages; NHTSA
AQ26002 opening resume; and the supplied book intake. You may return a newer
edition, a full primary document, or decisive contradictory context for a
covered topic, but label it as such.

For every candidate return a compact Markdown table row and a detailed entry:
- title, publisher/author, publication date, direct URL, source type,
  jurisdiction, and access status;
- which evidence contract it informs;
- exact bounded proposition it can support or challenge;
- a locator (section/page/figure/timestamp) and a quotation no longer than 20
  words where search-grounded context permits;
- whether it is primary/independent, why it is non-duplicate, and all material
  limitations;
- for visuals, media type, direct asset/page URL, visible claim and explicit
  rights/licensing uncertainty.

Provide a separate 'attempted to defeat the thesis' section: name any public
method that appears end-to-end, then state which assurance contracts it covers
and which it leaves open. Separate: no result found; source inaccessible;
source proprietary; and source does not meet the criterion. Never turn a
failed search into a claim of nonexistence.

Do not fabricate source text, certifications, approval status, URLs, dates,
or citations. If a claim needs an uninspected full document, say so plainly.
End with a ranked list of the ten best retrieval targets for a human/integrator.

PROJECT STATE PACKET:\n""" + json.dumps(packet, ensure_ascii=False)

    client = genai.Client(api_key=require("GEMINI_API_KEY"))
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        temperature=0.2,
    )
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=prompt,
        config=config,
    )
    stamp = date.today().isoformat()
    (OUT / f"grounded_response_{stamp}.md").write_text(response.text or "", encoding="utf-8")
    dump = response.model_dump(mode="json", exclude_none=True)
    (OUT / f"grounded_response_{stamp}.json").write_text(
        json.dumps(dump, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / f"prompt_{stamp}.txt").write_text(prompt, encoding="utf-8")
    print(f"Saved Gemini grounded discovery output to {OUT}")


if __name__ == "__main__":
    main()
