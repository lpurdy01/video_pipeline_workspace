"""Print the key numbers from reference_ladder_results.json for writing up findings."""
import json
import math
from pathlib import Path

d = json.loads((Path(__file__).parent / "reference_ladder_results.json").read_text())
print("cpu-min", round(d["cpu_seconds"] / 60), "wall-min", round(d["wall_seconds"] / 60), "FTLE", d["ftle"])
f = lambda x: "—" if x is None else (f"{x/1e3:.1f}k" if x >= 1e3 else f"{x:.0f}")
print(f"{'task':12} {'P10%':>7} {'P3%':>7} {'P1%':>7} {'P.3%':>7} | {'D10%':>7} {'D3%':>7} {'D1%':>7} {'D.3%':>7} | bmin bits_used  best_nrmse  D1/P1")
for t in d["tasks"]:
    p, dm, q = t["p_min"], t["d_min"], t["quant"]
    best = min(c["nrmse"] for c in t["capacity"])
    ratio = (dm["0.01"] / p["0.01"]) if dm["0.01"] and p["0.01"] else None
    print(f"{t['id']:12} " + " ".join(f"{f(p[k]):>7}" for k in ["0.1", "0.03", "0.01", "0.003"]) + " | "
          + " ".join(f"{f(dm[k]):>7}" for k in ["0.1", "0.03", "0.01", "0.003"])
          + f" | {q['b_min']!s:>4} {f(q['bits_used']):>9}  {best:.4f}  {'' if ratio is None else f'{ratio:.2f}'}")
for pre in ["pend", "dpend"]:
    for e in ["0.1", "0.03", "0.01"]:
        row = [next(t for t in d["tasks"] if t["id"] == f"{pre}_k{k}")["p_min"][e] for k in [1, 2, 4, 8, 16]]
        print(pre, e, [f(x) for x in row])

# Size exponent a in MSE ∝ P^(−a), fitted on the at-most-P frontier between 30% NRMSE and 1.5× the task's floor.
# Inverted: parameters needed ∝ loss^(−1/a), so halving the loss costs 2^(1/a)× the parameters.
# Language transformers sit at a ≈ 1/3 (Liu et al., arXiv:2602.05970). See scaling_mechanisms_findings.md.
print(f"\n{'task':12} {'pts':>3} {'a':>5} {'se':>5} {'P× per ½ loss':>14}")
for t in d["tasks"]:
    by = {}
    for c in t["capacity"]:
        by.setdefault(c["params"], []).append(c["nrmse"])
    fr, best = [], math.inf
    for p, e in sorted((p, min(v)) for p, v in by.items()):
        if e < best:
            best = e
            fr.append((p, e))
    use = [(math.log(p), 2 * math.log(e)) for p, e in fr if 1.5 * best <= e <= 0.3]
    if len(use) < 3:
        print(f"{t['id']:12} {len(use):>3}   too few frontier points")
        continue
    n, mx, my = len(use), sum(x for x, _ in use) / len(use), sum(y for _, y in use) / len(use)
    sxx = sum((x - mx) ** 2 for x, _ in use)
    b = sum((x - mx) * (y - my) for x, y in use) / sxx
    se = math.sqrt(sum((y - my - b * (x - mx)) ** 2 for x, y in use) / max(n - 2, 1) / sxx)
    print(f"{t['id']:12} {n:>3} {-b:>5.2f} {se:>5.2f} {2 ** (-1 / b):>14.2f}")

for pre in ["pend", "dpend"]:
    print(pre, "best nrmse by horizon", [round(min(c["nrmse"] for c in next(t for t in d["tasks"] if t["id"] == f"{pre}_k{k}")["capacity"]), 4) for k in [1, 2, 4, 8, 16]])
