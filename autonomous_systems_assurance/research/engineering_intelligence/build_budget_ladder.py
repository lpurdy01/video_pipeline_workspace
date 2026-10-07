"""Build the task-description ladder dataset for the intelligence-budget page.

Every row records the description form, the size as stored, the conversion used to get bits,
the source, a locator and a verification status:
  verified            - number checked in the original source text during this pass
  atlas-verified      - taken from the earlier pinned TorchVision/cross-domain atlas records
  documented          - widely documented value; locator supplied by the Gemini ladder scout, not re-inspected
  secondary           - press or secondary figure citing a primary report
  definitional        - follows from the form itself (e.g., a PID law has three gains)
Bits are an upper bound on task description length, never an estimate of it.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "interactive/src/data/budget_ladder.json"
TV = "https://docs.pytorch.org/vision/0.17/models/generated/torchvision.models."
LI = "https://arxiv.org/abs/1804.08838"
JULIAN = "https://arxiv.org/abs/1810.04240"


def row(id, name, task, domain, form, bits, basis, metric, year, url, locator, status,
        recognizable=False, series=None, fidelity=None, params=None):
    return dict(id=id, name=name, task=task, domain=domain, form=form, bits=bits, basis=basis,
                metric=metric, year=year, source_url=url, locator=locator, status=status,
                recognizable=recognizable, series=series, fidelity=fidelity, params=params)


R = []
add = R.append
# --- Hand-written laws (definitional: count of free constants x 32-bit float)
add(row("L-PID", "PID loop", "Regulate one variable", "control", "formula", 3 * 32, "3 gains × 32 bits",
        "Tuned per plant", 1942, "https://doi.org/10.1115/1.4019264", "Ziegler & Nichols 1942 (form only)",
        "definitional", True, params=3))
add(row("L-LQR", "LQR cart-pole", "Balance an inverted pendulum", "control", "formula", 4 * 32,
        "4-gain state feedback × 32 bits", "Stabilizing gain", 1960, "https://doi.org/10.1007/BF02788648",
        "u = −Kx with K ∈ R^(1×4)", "definitional", True, params=4))
add(row("L-KF", "2-state Kalman tracker", "Track position/velocity", "estimation", "formula", 2 * 32,
        "2 steady-state gains × 32 bits", "MMSE under model", 1960, "https://doi.org/10.1115/1.3662552",
        "Kalman 1960 (form only)", "definitional", params=2))
# --- Measured intrinsic dimension (Li et al. 2018, Table 1): d_int90 degrees of freedom × 32 bits
for rid, name, task, dom, d, rec, loc in [
    ("D-PEND", "Inverted pendulum (learned)", "Balance, 90% of full reward", "control", 4, True, "Table 1, Inverted Pendulum FC"),
    ("D-MNIST-LENET", "MNIST · LeNet", "Digits, 90% of baseline accuracy", "vision", 290, True, "Table 1, MNIST LeNet"),
    ("D-MNIST-FC", "MNIST · FC", "Digits, 90% of baseline accuracy", "vision", 750, False, "Table 1, MNIST FC"),
    ("D-HUMANOID", "Humanoid locomotion", "Walk, 90% of full reward", "control", 700, False, "Table 1, Humanoid FC"),
    ("D-CIFAR-RESNET", "CIFAR-10 · ResNet", ">50% accuracy", "vision", 1000, False, "§3.2 text, ResNet ≈1k"),
    ("D-CIFAR-LENET", "CIFAR-10 · LeNet", "90% of baseline", "vision", 2900, False, "Table 1, CIFAR-10 LeNet"),
    ("D-CIFAR-FC", "CIFAR-10 · FC", "90% of baseline", "vision", 9000, False, "Table 1, CIFAR-10 FC"),
    ("D-PONG", "Atari Pong", "90% of full score", "control", 6000, True, "Table 1, Atari Pong ConvNet"),
    ("D-MNIST-SHUF", "MNIST, shuffled labels", "Memorize 50k random labels (training fit)", "vision", 190000, True, "Table 1 and §3.1"),
    ("D-IMAGENET", "ImageNet · SqueezeNet", "90% of baseline (lower bound)", "vision", 500000, True, "§3.2: 'over 500k'"),
]:
    add(row(rid, name, task, dom, "learned subspace", d * 32, f"d_int90 = {d:,} × 32 bits", task, 2018, LI, loc,
            "verified", rec, series="intrinsic", params=d))
# --- ACAS Xu: one task, four descriptions (Julian, Kochenderfer & Owen)
add(row("A-TABLE", "ACAS Xu DP table (full)", "Horizontal collision advisories", "aviation", "lookup table",
        100e9 * 8, "'hundreds of gigabytes' → ≥100 GB", "Reference policy", 2016, JULIAN, "§II, 'hundreds of gigabytes'",
        "verified", True, series="acas", fidelity=1.0))
add(row("A-DOWN", "ACAS Xu table (downsampled)", "Horizontal collision advisories", "aviation", "lookup table",
        600e6 * 32, "600M floats × 32 bits (>2 GB)", "Reference after downsampling", 2016, JULIAN,
        "§II, '600 million floating point numbers… over 2GB'", "verified", True, series="acas", fidelity=1.0))
add(row("A-TREE", "ACAS Xu decision tree", "Horizontal collision advisories", "aviation", "decision tree",
        2.56e6 * 8, "2.56 MB tree", "Trees ≤100 MB: RMSE >3, policy error >6%", 2016, JULIAN, "§II and Fig. 2",
        "verified", False, series="acas", fidelity=0.94))
add(row("A-NET", "ACAS Xu neural networks", "Horizontal collision advisories", "aviation", "network",
        2.4e6 * 8, "2.4 MB floating point (≈45 × 11k params)", "Accurate table values; '1000×' smaller", 2016, JULIAN,
        "Abstract; §II '2.4 MB'; §IV '11000 parameters'", "verified", True, series="acas", fidelity=0.99,
        params=495000))
# --- AlexNet-level and VGG ImageNet: same accuracy, shrinking descriptions
add(row("C-ALEX", "AlexNet (fp32)", "ImageNet, 56.5% top-1", "vision", "network", 61.1e6 * 32,
        "61.1M params × 32 bits", "56.5% top-1", 2012, TV + "alexnet.html", "TorchVision 0.17 table", "atlas-verified",
        True, series="alexnet", fidelity=56.5, params=61.1e6))
add(row("C-ALEX-DC", "AlexNet, Deep Compression", "ImageNet, same accuracy", "vision", "compressed network",
        6.9e6 * 8, "6.9 MB after prune + quantize + Huffman", "'without loss of accuracy'", 2015,
        "https://arxiv.org/abs/1510.00149", "Abstract: 240 MB → 6.9 MB", "verified", True, series="alexnet", fidelity=56.5))
add(row("C-SQZ", "SqueezeNet, compressed", "ImageNet, AlexNet-level", "vision", "compressed network", 0.5e6 * 8,
        "<0.5 MB", "'AlexNet-level accuracy'", 2016, "https://arxiv.org/abs/1602.07360", "Abstract", "verified",
        True, series="alexnet", fidelity=56.5))
add(row("C-VGG", "VGG-16 (fp32)", "ImageNet, 71.6% top-1", "vision", "network", 138.4e6 * 32,
        "138.4M params × 32 bits", "71.6% top-1", 2014, TV + "vgg16.html", "TorchVision 0.17 table", "atlas-verified",
        True, series="vgg", fidelity=71.6, params=138.4e6))
add(row("C-VGG-DC", "VGG-16, Deep Compression", "ImageNet, same accuracy", "vision", "compressed network",
        11.3e6 * 8, "11.3 MB", "'no loss of accuracy'", 2015, "https://arxiv.org/abs/1510.00149",
        "Abstract: 552 MB → 11.3 MB", "verified", False, series="vgg", fidelity=71.6))
# --- TorchVision recognizable models (fp32 as released)
for rid, name, p, acc, slug, rec in [
    ("T-R50V1", "ResNet-50 (2015 recipe)", 25.6e6, 76.13, "resnet50.html", True),
    ("T-R50V2", "ResNet-50 (2021 recipe)", 25.6e6, 80.858, "resnet50.html", True),
    ("T-MNV2", "MobileNetV2", 3.5e6, 71.878, "mobilenet_v2.html", True),
    ("T-MNAS", "MNASNet 0.75", 3.2e6, 71.18, "mnasnet0_75.html", False),
    ("T-EB0", "EfficientNet-B0", 5.3e6, 77.692, "efficientnet_b0.html", True),
    ("T-VITB", "ViT-B/16", 86.6e6, 81.072, "vit_b_16.html", True),
    ("T-CNXL", "ConvNeXt-Large", 197.8e6, 84.414, "convnext_large.html", False),
    ("T-VITL", "ViT-L/16 (SWAG)", 305.2e6, 88.064, "vit_l_16.html", True),
]:
    add(row(rid, name, f"ImageNet, {acc:.1f}% top-1", "vision", "network", p * 32, f"{p/1e6:.1f}M params × 32 bits",
            f"{acc:.1f}% top-1", None, TV + slug, "TorchVision 0.17 model table", "atlas-verified", rec,
            series="imagenet", fidelity=acc, params=p))
# --- Driving, aviation detection, face
add(row("N-ALVINN", "ALVINN", "Follow a road from a 30×32 camera + 8×32 range image", "driving", "network",
        (1217 * 29 + 29 * 46) * 32, "1,217→29→46 units ≈ 36.6k weights × 32 bits (float assumed)",
        "Road following under 'certain field conditions'", 1989,
        "https://proceedings.neurips.cc/paper/1988/hash/812b4ba287f5ee0bc9d43bbf5bbe87fb-Abstract.html",
        "Architecture section: 1217 inputs, 29 hidden, 46 outputs", "verified", True, params=1217 * 29 + 29 * 46))
add(row("N-PILOTNET", "NVIDIA PilotNet", "Steer from one camera", "driving", "network", 250e3 * 32,
        "≈250k params × 32 bits", "Lane keeping on test roads", 2016, "https://arxiv.org/abs/1604.07316",
        "Fig. 4 caption: '250 thousand parameters'", "verified", True, params=250e3))
add(row("N-YOLOV8S", "YOLOv8s (AVOIDDS)", "Detect intruder aircraft (synthetic)", "aviation", "network", 11.2e6 * 32,
        "11.2M params × 32 bits", "mAP 0.866 overall (baseline)", 2023, "https://arxiv.org/pdf/2306.11203",
        "§3–4; App. C Table 4", "atlas-verified", False, params=11.2e6))
add(row("N-MFN", "MobileFaceNet", "Face verification", "face", "network", 0.99e6 * 32, "0.99M params × 32 bits",
        "99.55% LFW; 92.59% TAR @ FAR 1e-6", 2018, "https://arxiv.org/pdf/1804.07573", "Abstract; Tables 3–4",
        "atlas-verified", True, params=0.99e6))
# --- Speech and language
for rid, name, p in [("W-TINY", "Whisper tiny", 39e6), ("W-BASE", "Whisper base", 74e6), ("W-SMALL", "Whisper small", 244e6),
                     ("W-MED", "Whisper medium", 769e6), ("W-LARGE", "Whisper large", 1550e6)]:
    add(row(rid, name, "Multilingual speech recognition", "speech", "network", p * 16, f"{p/1e6:,.0f}M params × 16 bits",
            "See paper WER tables", 2022, "https://arxiv.org/abs/2212.04356", "Table 1 (model sizes)", "verified",
            rid in ("W-TINY", "W-LARGE"), series="whisper", params=p))
add(row("G-CHIN", "Chinchilla", "Language modelling", "language", "network", 70e9 * 16, "70B params × 16 bits",
        "67.5% MMLU", 2022, "https://arxiv.org/abs/2203.15556", "Tables 1 and 6", "atlas-verified", True, params=70e9))
add(row("G-GOPH", "Gopher", "Language modelling", "language", "network", 280e9 * 16, "280B params × 16 bits",
        "60.0% MMLU", 2021, "https://arxiv.org/abs/2112.11446", "Hoffmann et al. comparison", "atlas-verified",
        False, params=280e9))
for rid, name, p, b, metric, url, rec in [
    ("G-GPT2XL", "GPT-2 XL", 1.5e9, 32, "Zero-shot LM benchmarks", "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf", False),
    ("G-GPT3", "GPT-3", 175e9, 16, "Few-shot benchmarks", "https://arxiv.org/abs/2005.14165", True),
    ("G-L3-8", "Llama 3 8B", 8e9, 16, "Open-weights LLM", "https://arxiv.org/abs/2407.21783", True),
    ("G-L3-70", "Llama 3 70B", 70.6e9, 16, "Open-weights LLM", "https://arxiv.org/abs/2407.21783", False),
    ("G-L3-405", "Llama 3.1 405B", 405e9, 16, "Open-weights LLM", "https://arxiv.org/abs/2407.21783", True),
    ("G-DSV3", "DeepSeek-V3 (MoE)", 671e9, 8, "Open-weights MoE LLM", "https://arxiv.org/abs/2412.19437", True),
    ("R-OPENVLA", "OpenVLA", 7e9, 16, "Robot manipulation policy", "https://arxiv.org/abs/2406.09246", False),
    ("R-PI0", "π0", 3.3e9, 16, "Robot manipulation policy", "https://arxiv.org/abs/2410.24164", False),
    ("S-AF2", "AlphaFold 2", 93e6, 32, "Protein structure", "https://doi.org/10.1038/s41586-021-03819-2", True),
]:
    dom = "robotics" if rid.startswith("R-") else ("science" if rid.startswith("S-") else "language")
    add(row(rid, name, metric, dom, "network", p * b, f"{p/1e9:,.2f}B params × {b} bits", metric, None, url,
            "Model size as widely reported; not re-inspected", "documented", rec, params=p))
add(row("K-7B", "Knowledge a 7B model can hold", "2 bits/param × 7B (Allen-Zhu & Li)", "language", "capacity estimate",
        14e9, "'a 7B model can store 14B bits of knowledge'", "Exceeds English Wikipedia + textbooks (authors' estimate)",
        2024, "https://arxiv.org/abs/2404.05405", "Abstract", "verified", True))
# --- Hand-written flight and vehicle software (upper bounds on description; conversions stated)
add(row("H-AGC", "Apollo Guidance Computer", "Lunar guidance, navigation and control", "aviation", "hand-written code",
        36864 * 16, "36,864 fixed-memory words × 16 bits", "Apollo missions", 1966,
        "https://ntrs.nasa.gov/citations/19880069935", "Tomayko, Computers in Spaceflight, ch. 2", "documented", True))
SLOC_BITS = 200  # stated conversion assumption: ~25 characters/line at ~1 bit/char after compression, ×8 rounding
for rid, name, sloc, url, loc, rec in [
    ("H-787", "Boeing 787 avionics + support", 6.5e6, "https://spectrum.ieee.org/this-car-runs-on-code", "Charette 2009", True),
    ("H-F35", "F-35 onboard software", 8e6, "https://spectrum.ieee.org/f35-program-continues-to-struggle-with-software", "IEEE Spectrum citing GAO", True),
    ("H-CAR", "Premium car software (2009)", 100e6, "https://spectrum.ieee.org/this-car-runs-on-code", "Charette 2009", False),
]:
    add(row(rid, name, "Vehicle functions (many, not one task)", "vehicle", "hand-written code", sloc * SLOC_BITS,
            f"{sloc/1e6:.1f}M SLOC × {SLOC_BITS} bits/line (assumed)", "In service", None, url, loc, "secondary", rec))

HW = [
    dict(id="HW-TESLA3", name="Tesla HW3 (per chip)", tops_int8=72, bw_gbs=68, mem_gb=None,
         status="vendor, Autonomy Day 2019 (01:21:40 bandwidth; 01:22:49 72 TOPS)", relative=None),
    dict(id="HW-TESLA3-BOARD", name="Tesla HW3 (two chips, redundant)", tops_int8=144, bw_gbs=136, mem_gb=None,
         status="vendor; two independent chips, not one model's resources", relative=None),
    dict(id="HW-XAVIER", name="NVIDIA Jetson AGX Xavier", tops_int8=32, bw_gbs=None, mem_gb=None,
         status="vendor peak (atlas)", relative=None),
    dict(id="HW-ORIN", name="NVIDIA Jetson AGX Orin", tops_int8=275, bw_gbs=204.8, mem_gb=64,
         status="vendor sparse INT8 peak (atlas); ≈half dense", relative=None),
    dict(id="HW-DRIVEORIN", name="NVIDIA DRIVE Orin", tops_int8=254, bw_gbs=200, mem_gb=None,
         status="vendor sparse INT8 peak (atlas)", relative=None),
    dict(id="HW-AI4", name="Tesla AI4", tops_int8=None, bw_gbs=None, mem_gb=None,
         status="no official absolute figure (reference = 0 dB)", relative=dict(compute=1, memory=1)),
    dict(id="HW-AI5", name="Tesla AI5 (target)", tops_int8=None, bw_gbs=None, mem_gb=None,
         status="vendor target relative to AI4: 10× compute, 9× memory, 50× total claim (Q4 2025 update p.10)",
         relative=dict(compute=10, memory=9, total_claim=50)),
]

RATES = [
    dict(id="RATE-SENSE", name="Human sensory intake", bits_per_s=1e9, url="https://arxiv.org/abs/2408.10234",
         status="verified (abstract)"),
    dict(id="RATE-BEHAV", name="Human behavioural throughput", bits_per_s=10, url="https://arxiv.org/abs/2408.10234",
         status="verified (abstract)"),
    dict(id="RATE-CAM", name="Eight 1280×960 cameras, 36 Hz, 8-bit mono", bits_per_s=8 * 1280 * 960 * 36 * 8, url=None,
         status="arithmetic, illustrative configuration"),
]

OUT.write_text(json.dumps(dict(
    note="Bits are description sizes as stored (upper bounds on task description length). Status field defines verification level.",
    rows=R, hardware=HW, rates=RATES), indent=1))
print(len(R), "rows;", sum(r["recognizable"] for r in R), "recognizable;",
      {s: sum(r["status"] == s for r in R) for s in sorted({r["status"] for r in R})})
