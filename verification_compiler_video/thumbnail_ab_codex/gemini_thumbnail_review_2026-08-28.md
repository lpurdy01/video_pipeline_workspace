# Gemini thumbnail review - 2026-08-28

Model: `models/gemini-3.1-pro-preview`

Here is the review of your thumbnail candidates based on the video’s thesis, audience, and the constraints of YouTube packaging.

## CTR Ranking
*(Ranked by ability to stop the scroll in a cold feed)*

1. **Candidate A (Who Checks It?):** This is the strongest hook. It taps directly into the current, visceral anxiety of the target audience (agentic devs/managers). Every senior engineer is currently worried about the tsunami of AI-generated code. It poses a high-stakes question.
2. **Candidate B (Chat Is Not Evidence):** Very strong runner-up. It uses a contrarian, almost combative hook. It directly attacks a common misconception (that LLMs grading themselves equals safety) and establishes instant authority.
3. **Candidate C (The Bottleneck Is Verification):** Too dry. It reads like a B2B whitepaper title. While factually true to your thesis, "bottleneck" is an analytical business term that doesn't trigger the immediate emotional curiosity of A or B. 
4. **Candidate D (Compiler For Trust):** Bluntly, this will tank with a cold audience. "Compiler for Trust" means nothing until they watch the video. You are pitching the *solution* before making them care about the *problem*. It feels like a university lecture.

## Promise-Match Ranking
*(Ranked by how accurately they represent the video's core technical thesis)*

1. **Candidate B (Chat Is Not Evidence):** Perfectly sets up the "trust the evidence surface, not the AI" boundary mentioned in your brief. It literally contrasts the wrong way (chat) with the right way (traceable record).
2. **Candidate D (Compiler For Trust):** Highly accurate to the actual architecture (showing the Verification Query Package graph), even though it fails as a top-of-funnel hook.
3. **Candidate C (Bottleneck Is Trust):** Accurately represents the macro-economic shift of code generation vs. software assurance.
4. **Candidate A (Who Checks It?):** Accurately sets up the premise, but the visual (shapes flying at a wall) is more of a metaphor than a representation of the actual traceability solution.

## Mobile Legibility
* **Candidate A:** The main text is massive and excellent. However, the background visual chaos is a bit muddy at small sizes, though the red standard line and the '?' do survive scaling.
* **Candidate B:** Outstanding text legibility. The background code/chat text is entirely illegible at mobile size, *but that doesn't matter*—the structural framing and the red X / green checkmark communicate the visual story perfectly without needing to read the code.
* **Candidate C:** The cyan text on dark background has a slight visual vibration. The complex graph on the right turns to mush on mobile.
* **Candidate D:** The main text is readable, but the subtitle pill (`GRAPH -> PACKAGE -> EVIDENCE`) and the node labels (`SRC`, `CODE`, `TEST`) are far too small. At mobile size, it just looks like random colored lines.

## Best A/B Test
**Run Candidate A vs. Candidate B.**

These two test genuinely different psychological motivations for clicking:
* **Candidate A (Anxiety/Overwhelm):** Tests if the audience is driven by the pain point of their current workflow breaking down under the volume of AI code.
* **Candidate B (Contrarian/Rigor):** Tests if the audience is driven by a desire for professional standards, targeting the frustration of treating "chatbots" as engineering tools.

*Discard C and D for the primary launch. They are too abstract and lack emotional immediacy.*

## Fixes
Before exporting the final files for the A/B test, make these exact tweaks:

**For Candidate A:**
* **Thicken the "Standard" barrier:** The two vertical yellow lines and the word "STANDARD" need to be 30% thicker/bolder. At mobile size, the difference between the "mess" on the left and the "filter" on the right needs to be stark.
* **Clean the clutter:** Remove the faint, tiny white text floating near the top right of the yellow lines. It adds nothing and creates noise.

**For Candidate B:**
* **Delete the ghost text:** Remove the faint grey text at the very top ("One of these can be audited"). It is unreadable on mobile and distracts from the massive main title.
* **Scale up the icons:** Increase the size of the bottom Red X and Green Checkmark by at least 50%. They are the primary visual anchors for the "Not Evidence / Evidence" dichotomy at small scale. 

## Final Recommendation
Launch with the **A vs. B** test using the suggested fixes. 

Candidate A’s title ("AI Can Write Code. Who Checks It?") paired with its thumbnail is the most likely to pull in the "technically curious" broader audience, while Candidate B will absolutely nail the "safety-critical/software-assurance" niche. Let the YouTube algorithm decide which audience is hungrier.
