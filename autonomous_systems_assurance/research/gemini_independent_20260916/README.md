# Independent Gemini grounded-research space

This space is an independent discovery and challenge pass. It is not a research contribution and may not directly create project claims. The Gemini response is saved under the ignored `out/` directory, then the integrator must retrieve, hash, inspect and independently classify every candidate before it can enter a lane registry.

The run brief deliberately distinguishes frozen trained models from models that learn in operation, excludes speculation about proprietary implementations, and asks Gemini to find public citable material absent from the current inventory. It asks for sources that could **defeat** the project's current partial-toolkit framing as well as sources that identify its limits.

Run `python3 run_grounded_research.py` from this directory. It uses the user-approved Gemini API credential through `workspace_credentials.require("GEMINI_API_KEY")`, requests Google Search grounding when the installed Gemini SDK supports it, and writes no credential into the workspace. A network/API failure is recorded in the process output and does not count as a negative research result.

