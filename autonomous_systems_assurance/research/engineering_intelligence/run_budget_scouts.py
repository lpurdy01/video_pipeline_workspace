"""Grounded Gemini scouts for the condensed 'intelligence budget' hypothesis.

Three sequential calls (one worker, >=20 s apart, stop on 429, per D-024):
  sources   - verify grounding sources and their key numbers/locators
  ladder    - candidate data points for a task-description-size ladder
  challenge - adversarial mathematical check of the condensed framework
Raw prompts and responses stay under ignored out/. Output is lead material, never evidence.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SPACE = Path(__file__).resolve().parent
sys.path.insert(0, str(SPACE.parents[2]))
from workspace_credentials import require  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

COMMON = """Date context: September 2026. Use Google Search grounding. Cite ORIGINAL sources
(arXiv abs/html, journal DOI, official documentation) with exact locators (section, table,
figure, theorem, page). Quote at most 25 words per quotation. Never invent numbers, URLs or
locators; write 'not found in this search' instead. Flag vendor claims separately from
peer-reviewed results.
"""

SOURCES = COMMON + """
We are building a hypothesis that measures every resource of a learned system in BITS:
task description length K(eps) needed to reach error eps; model storage capacity kappa*P
(bits per parameter times parameters); training information delivered by data; observation
information preserved by sensors; and evidence bits for rare-event claims. Verify each lead below.
For each: confirm it exists, give authors/venue/year/URL, the exact numerical result and its
locator, the assumptions, and one sentence on what it does NOT show.

1. Allen-Zhu & Li, "Physics of Language Models: Part 3.3, Knowledge Capacity Scaling Laws"
   (reported ~2 bits of knowledge per parameter). Conditions (training exposures, int8, MoE).
2. Morris et al. 2025, "How much do language models memorize?" (reported ~3.6 bits/parameter).
3. Boelcskei, Grohs, Kutyniok, Petersen 2019, "Optimal Approximation with Sparsely Connected
   Deep Neural Networks" and Elbraechter, Perekrestenko, Grohs, Boelcskei 2021 "Deep Neural
   Network Approximation Theory" (IEEE Trans. Inf. Theory): the Kolmogorov-Donoho
   rate-distortion lower bound on connectivity/memory of networks with quantized weights.
   State the theorem precisely (optimal exponent gamma*, polylog bits per weight).
4. Kolmogorov & Tikhomirov 1959 epsilon-entropy of function classes (Sobolev/Hoelder balls
   scale like eps^(-d/s)); a modern accessible statement.
5. Achille, Paolini, Mbeng, Soatto, "The Information Complexity of Learning Tasks, their
   Structure and their Distance" (task complexity via structure function / information in weights).
6. Lotfi et al. 2022 "PAC-Bayes Compression Bounds So Tight That They Can Explain
   Generalization" and Lotfi et al. 2023/2024 LLM bounds: concrete compressed sizes in bits
   for models reaching stated accuracy (e.g., MNIST, CIFAR-10, ImageNet).
7. Li et al. 2018 intrinsic dimension of objective landscapes: exact d_int90 numbers for
   MNIST, CIFAR-10, ImageNet, and RL tasks (e.g., cartpole, Atari Pong).
8. Michaud et al. 2023 quantization model of neural scaling: the predicted relation between
   the parameter-scaling exponent and the data-scaling exponent (is it alpha_D = alpha_N/(alpha_N+1)?).
   Compare with Hoffmann et al. 2022 fitted alpha=0.34, beta=0.28 and Kaplan et al. 2020.
9. "Densing Law of LLMs" (Xiao et al. 2024): capability density doubling period and definition.
10. Algorithmic progress: Ho et al. 2024 (language models, compute halving time) and
    Erdil & Besiroglu 2022 (computer vision, ImageNet). Exact halving times and CIs.
11. Test-time compute versus parameters: Snell et al. 2024; and Merrill & Sabharwal 2024
    "The Expressive Power of Transformers with Chain of Thought" (serial depth via CoT).
12. Gell-Mann & Lloyd 1996 "Information measures, effective complexity, and total
    information"; Bennett 1988 logical depth. One-sentence definitions with locators.
13. Johnson criteria (Johnson 1958) for detection/recognition/identification in line pairs
    or pixels on target, and the modern Targeting Task Performance (TTP) metric
    (Vollmerhausen/Driggers). Exact cycle numbers for 50% probability.
14. Gong, Boddeti & Jain 2019 "On the Capacity of Face Representation" (IEEE TPAMI): capacity
    numbers (identities at a false accept rate) for named representations.
15. Julian, Kochenderfer, Owen 2018/2019 ACAS Xu network compression: table size, network
    size, compression factor, and fidelity.
16. LeCun's 'cake' slide (NIPS 2016 keynote): bits of supervision per sample for RL,
    supervised and self-supervised learning. Also any peer-reviewed treatment of
    'supervision bits per example' and dense auxiliary supervision in driving.
17. Fano's inequality stated as a lower bound on error from mutual information.
18. Any published work that already frames model size requirements as a rate-distortion
    function of the task, or a 'link budget' style feasibility analysis for ML on edge
    hardware. Also any work tying operational-domain restriction to finite task complexity.

End with a table: lead | verified? | key number | locator | URL.
"""

LADDER = COMMON + """
We want a 'task description ladder': 40-60 systems that each solve a recognizable task, placed
on a log scale by the SIZE of their task description in bits: hand-written formulas, control
laws, lookup tables, flight/automotive software, and learned networks (parameters x stored bits).
For each candidate give: system; task; description form (formula/table/code/network);
size (parameters, lines of code, words of memory, table bytes) with the exact figure;
stored precision if known; performance metric and value; year; primary source URL and locator.
Prefer primary sources (papers, official docs, NASA/GAO reports, model cards). Mark any figure
that is only from press or secondary sources.

Include at least:
- Classical control: PID loop (3 gains), LQR/Kalman examples, Apollo Guidance Computer memory
  (fixed/erasable words, word size), Space Shuttle flight software size, F-35 and Boeing 787
  software lines of code (GAO or similar).
- Aviation ML: ACAS Xu score tables vs compressed networks; any DAA/vision detector sizes.
- Driving: ALVINN (1989) weights and input size; NVIDIA PilotNet/DAVE-2 parameters; comma.ai
  openpilot driving model (supercombo) parameter count/file size and hardware; Tesla HW3/HW4(AI4)
  public compute figures (vendor) and any public statement of FSD network size (flag if none).
- Vision: LeNet-5, AlexNet, VGG-16, ResNet-50, MobileNetV2, EfficientNet-B0, ViT-B/16, YOLOv8
  sizes, DINOv2, SAM; with ImageNet/COCO accuracy.
- Face: FaceNet NN2, MobileFaceNet, ArcFace ResNet-100.
- Speech/language: Whisper tiny..large, GPT-2, GPT-3, Chinchilla, Gopher, Llama 3 8B/70B/405B,
  DeepSeek-V3 (total vs active), and their key benchmark numbers.
- Games/science: AlphaGo Zero, AlphaZero, Stockfish NNUE net size, AlphaFold 2.
- Robotics: RT-1, RT-2, OpenVLA, pi0 parameter counts.
Also list 6-10 edge inference hardware anchors with peak INT8 TOPS, memory bandwidth and
memory capacity from official specs: Tesla HW3 (vendor), NVIDIA Jetson Orin Nano/NX/AGX, DRIVE
Orin, DRIVE Thor, Qualcomm Snapdragon Ride, Mobileye EyeQ5/EyeQ6, Hailo-8.
Return a compact table first, then notes on uncertain rows.
"""

CHALLENGE = COMMON + """
Act as an adversarial mathematician and ML theorist. Check this condensed hypothesis. Label
each step: theorem (under stated assumptions), empirical fit, or new hypothesis. Find errors,
missing assumptions, and counterexamples. Suggest better formulations. Be concise and precise.

H0 (currency). Measure all resources in bits. Under log loss the Bayes floor is H(Y|O); Fano
links mutual information I(O;Y) to a minimum classification error.

H1 (task spectrum). A task in an operating domain is a set of reusable skills k with
frequency p_k (sum to 1), loss reduction Delta_k when learned, description cost c_k bits and
serial depth d_k. Learning proceeds roughly in order of p_k*Delta_k/c_k.
Achievable error: eps(P,D,L) = eps_floor(O) + sum_{k not learned} p_k Delta_k, where learned
set requires: sum c_k <= kappa*P (storage), D*p_k*s >= c_k*r (data: s supervision bits per
example, r a redundancy/learning inefficiency factor), and d_k <= depth affordable within
deadline L.

H2 (power law). If p_k ~ k^-(1+g) with constant c and Delta: eps_P ~ (kappa P / c)^-g,
eps_D ~ (D s/(c r))^(-g/(1+g)). So predicted beta = alpha/(1+alpha). Compare to Hoffmann
alpha=0.34, beta=0.28 (0.34/1.34=0.254) and to Michaud et al.

H3 (ODD truncation). Restricting the operating domain truncates the spectrum at k_max, giving
finite K_total = sum c_k; scaling then saturates (broken/saturating scaling laws).

H4 (single feasibility inequality). For a dense model processing T tokens per decision at
deadline L with effective compute C and bandwidth B and b-bit weights, P_max = min(8M/b,
8BL/b, CL/(2T)). Required P_min(eps) = K(eps)/kappa with K(eps) = sum of c_k over skills
needed for eps. Feasible iff K(eps) <= kappa * P_max. 'Intelligence margin' = 10 log10(
kappa P_max / K(eps)) dB, analogous to an RF link budget margin.

H5 (supervision bandwidth). A driving policy supervised only with 2 continuous actions per
frame, most of which are 'go straight', gets few task bits per example (large r), so rare
skills fail the data condition; dense auxiliary tasks (segmentation, depth, occupancy, video
prediction) raise s and so lower the exposure needed per skill. This is our interpretation of
Tesla's 2026 'proxy tasks' statement and LeCun's 'cake' picture.

H6 (limit band). The theoretical ceiling uses kappa = b (every stored bit useful; related to
Kolmogorov-Donoho bounds for quantized networks); empirical frontier kappa ~2-3.6
bits/param (Allen-Zhu & Li; Morris et al.); a release sits below. Gap to limit in dB is
analogous to a code's gap to the Shannon limit.

H7 (evidence). Zero failures in n independent hazard trials bounds p below ln(1/a)/n at
confidence 1-a; each trial supplies about p*log2(e) bits of evidence against p >= p_target.

Questions: (a) Is H2's exponent relation right and is it in Michaud et al.? (b) What is wrong
with using kappa=b as a 'theoretical ceiling'? (c) Is K(eps) well defined across
architectures, and how should architecture/inductive bias enter (a per-family kappa?) (d) Does
H4 double count or omit attention/activation cost and serial depth? (e) Is H5 consistent with
information theory (bits of supervision vs bits learned)? (f) Propose the minimal set of
dimensionless numbers (like Reynolds numbers) that captures H1-H7, and the three most
decisive experiments to falsify the framework.
"""


SOURCES2 = COMMON + """
Short, precise answers only; one table row per item, then 2-4 sentences of notes per item.
Verify each and give the exact number, locator and URL:
1. PRIOR ART. Works that derive neural scaling laws from information theory or rate-distortion
   (e.g., Jeon & Van Roy, 'Information-Theoretic Foundations for Neural Scaling Laws', 2024;
   Hutter 2021 'Learning Curve Theory'; any 'rate-distortion view of model size'). What exactly
   do they assume and derive? Is 'model size ~ task rate-distortion / bits-per-parameter' already
   proposed anywhere?
2. Johnson criteria: cycles (line pairs) across the critical dimension for 50% probability of
   detection, orientation, recognition, identification (Johnson 1958, 'Analysis of image forming
   systems'); the modern TTP metric (Vollmerhausen & Jacobs, NVESD); primary or DTIC URLs.
3. LeCun 'cake' slide numbers of bits per sample for RL, supervised and self-supervised learning.
4. Ma et al. 2024 'The Era of 1-bit LLMs' (BitNet b1.58): parameter size at which ternary
   weights match FP16 LLaMA; and Allen-Zhu & Li 3.3 result for int4 capacity (bits/param).
5. Carlsmith 2020 (Open Philanthropy) brain-compute estimate range and median FLOP/s; Koch et al.
   2006 'How much the eye tells the brain' (retina to brain bits/s).
6. Tesla HW3 FSD chip (Bannon et al., Hot Chips 31, 2019 and IEEE Micro 2020): TOPS per chip,
   DRAM type/bandwidth, SRAM, power. Any official AI4/HW4 compute or bandwidth figure (flag if none).
7. Cover 1965 perceptron capacity (2N patterns for N weights): exact statement and source.
8. Landauer limit value at 300 K (J per bit) and any source comparing current accelerator
   energy per operation to it.
9. Gell-Mann & Lloyd 1996 effective complexity and Bennett 1988 logical depth: one-sentence
   definitions with primary source URLs.
"""


CHAOS = COMMON + """
Short, precise answers; a table first, then 2-4 sentences per item. We are running a laptop-scale
experiment: fit MLPs (2 hidden layers, width 2-256) to reference functions of increasing complexity
(PID law, saturated PID, pendulum one-step map, cart-pole step, double-pendulum step, the pendulum
step observed through two rendered 24x24 camera frames) and to the t-step flow maps of a regular
pendulum versus a chaotic double pendulum for t = 50-800 ms. We record the smallest width and the
smallest training set reaching test NRMSE thresholds (10%, 3%, 1%, 0.3%) and the weight bits used
after quantization. Find and verify:
1. Prior work measuring the network size (or number of parameters/basis functions/reservoir size) needed
   to approximate or forecast a chaotic system as a function of forecast horizon or Lyapunov time
   (e.g., Pathak et al. 2018 reservoir computing; Vlachas et al.; Gilpin 2021/2023 chaos benchmarks).
   Any theorem that approximating the time-t flow map needs complexity growing like exp(lambda t)?
2. Approximation-theory results for Lipschitz/Sobolev functions giving network size ~ (L/eps)^(d/s),
   so that a Lipschitz constant growing as exp(lambda t) implies exponential size growth.
3. Sample-complexity results for learning dynamics (system identification) with neural networks:
   examples needed versus model size and accuracy; any 'examples per parameter' empirical rule.
4. Physics-informed or structured inputs (e.g., Hamiltonian/Lagrangian neural networks, sin/cos
   features) reducing parameters or data needed for pendulum/double pendulum.
5. Vision-based dynamics learning (pixels to state, e.g., 'visual interaction networks', pixel
   pendulum benchmarks): how much larger models/data are than state-based versions.
6. Critique our experimental design: what confounds (optimizer, training steps, input normalization,
   angle wrapping, target scaling, seeds) could make 'minimum width' misleading, and how to mitigate
   within a CPU budget of about 1-2 hours.
"""


def run(client, name: str, prompt: str) -> None:
    out = SPACE / "out"
    out.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (out / f"budget_{name}_prompt_{stamp}.txt").write_text(prompt)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
            temperature=0.1,
        ),
    )
    (out / f"budget_{name}_response_{stamp}.md").write_text(response.text or "")
    (out / f"budget_{name}_response_{stamp}.json").write_text(
        json.dumps(response.model_dump(mode="json", exclude_none=True), indent=2)
    )
    print(f"{name}: saved budget_{name}_response_{stamp}.md", flush=True)


def main() -> None:
    wanted = sys.argv[1:] or ["sources", "ladder", "challenge"]
    prompts = {"sources": SOURCES, "ladder": LADDER, "challenge": CHALLENGE, "sources2": SOURCES2, "chaos": CHAOS}
    client = genai.Client(api_key=require("GEMINI_API_KEY"))
    for i, name in enumerate(wanted):
        if i:
            time.sleep(20)
        try:
            run(client, name, prompts[name])
        except Exception as exc:  # stop on quota/credit errors rather than retrying
            print(f"{name}: failed: {exc}", flush=True)
            if "429" in str(exc) or "402" in str(exc):
                break


if __name__ == "__main__":
    main()
