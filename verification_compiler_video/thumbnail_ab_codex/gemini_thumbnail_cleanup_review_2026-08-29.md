# Gemini thumbnail review - 2026-08-29

Model: `models/gemini-3.1-pro-preview`

Here is the review of the thumbnail and packaging candidates, evaluated against your goals and the lessons learned from the previous launch.

## CTR Ranking

1. **Candidate A (Who Checks The Code?)**: This is the strongest hook for a cold feed. It taps directly into the current, immediate anxiety of engineering managers and senior devs: we opened the floodgates to AI code, but we haven't scaled our review process. The curiosity gap is highly relatable.
2. **Candidate B (Chat Is Not Evidence)**: A very strong runner-up. It takes a contrarian, opinionated stance that will resonate deeply with the safety-critical and high-assurance crowd who are annoyed by AI hype. It demands a click to see how you prove it.
3. **Candidate D (Compiler For Trust)**: This will get clicks from architecture nerds already warm to you, but it's a "solution" hook rather than a "problem" hook. It lacks the emotional urgency of A or B for a cold audience.
4. **Candidate C (Trust Is The Bottleneck)**: To be blunt, this candidate is boring. The phrase reads like a generic corporate slide, and the visuals are purely abstract shapes with no emotional weight. It will get scrolled past.

## Promise-Match Ranking

1. **Candidate D**: Literally maps out the video's core technical thesis (the traceability graph of Req -> Code -> Test -> VQP -> Evidence). It is a perfect promise-match for the proposed Verification Compiler.
2. **Candidate B**: Perfectly matches the philosophical boundary of the video: we are not trusting the AI, we are trusting the evidence surface. The visual dichotomy of unstructured chat vs. structured artifact hits the nail on the head.
3. **Candidate A**: Accurately frames the *problem* the video solves, but does not hint at the specific technical solution (the compiler/traceability). 
4. **Candidate C**: Captures the macroeconomic premise but offers nothing about the actual technical implementation or workflow.

## Mobile Legibility

*   **Candidate A**: Excellent. The massive white and pink text is highly legible. The red question mark serves as a great visual anchor even when tiny. The sub-badge ("AI CAN WRITE IT") is readable.
*   **Candidate B**: The main headline and the red X / green Checkmark read perfectly at small sizes. However, the actual text *inside* the chat and code windows is completely illegible on mobile. The visual layout does the heavy lifting, but the tiny text adds clutter.
*   **Candidate D**: The main title is strong. However, the crucial technical details—the text inside the graph nodes (REQ, CODE, TEST, VQP)—are too small to read on a phone. The sub-badge ("AI REVIEW + HUMAN AUTHORITY") is also borderline unreadable.
*   **Candidate C**: Text is readable, but the abstract visuals turn into a meaningless blur at thumbnail size.

## Best A/B Test

**Candidate A vs. Candidate B**

This pairing tests two distinct and powerful viewer motivations:
*   **Variant A ("Who Checks The Code?")** tests **Anxiety/Overwhelm**: It targets the viewer's fear of the massive volume of unverified generated code.
*   **Variant B ("Chat Is Not Evidence")** tests **Rigor/Contrarianism**: It targets the viewer's annoyance at sloppy, unstructured AI workflows and appeals to their desire for engineering discipline.

Both are emotionally immediate, but they come at the problem from different psychological angles. (Do not test C, and D requires too much reading for a cold feed test).

## Fixes

Before exporting the final versions for the A/B test, make these exact adjustments:

**For Candidate A:**
*   **Brighten the red/pink text:** "THE CODE?" is slightly dark against the pure black background. Push the brightness/saturation up slightly so it punches through as much as the white text.
*   **Thicken the question mark:** Ensure the stroke on the red question mark is thick enough to survive heavy compression on mobile screens.

**For Candidate B:**
*   **Abstract the UI text:** Since no one can read the text inside the dark chat window or the green code window on mobile, stop trying to make it real text. Replace it with abstract "skeleton UI" blocks (e.g., thick grey bars for chat, brightly colored syntax-highlighted bars for the JSON). This removes visual clutter while keeping the layout recognizable.
*   **Enlarge the X and Checkmark:** Scale these up by 15-20%. They are the primary visual communicators of "Bad vs. Good" and need to be unmistakable at a glance.

## Final Recommendation

Run an A/B test on YouTube using **Candidate A** and **Candidate B** after applying the fixes above. 

Candidate A is your safest bet for maximum reach, as it asks a question every developer is currently feeling. Candidate B is your best bet for high-retention clicks from your core demographic of senior, safety-critical engineers. Let the YouTube algorithm decide which hook pulls better from the cold feed. Discard C entirely, and save the graph from D for an in-video title card or community post.
