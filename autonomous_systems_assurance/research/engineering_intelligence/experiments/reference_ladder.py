"""Reference-function ladder: how large a network, and how much data, to fit a known function?

Each task is a known reference function sampled on a box of inputs:
  PID law -> saturated PID -> pendulum step -> cart-pole step -> double-pendulum step,
  pendulum / double-pendulum flow maps at longer horizons (regular vs chaotic),
  the pendulum step with a physics feature prior, and the pendulum step seen only through
  two rendered 24x24 camera frames.

For each task we sweep MLP width (capacity) and training-set size (data), train with early stopping
on an independent validation set, and report test NRMSE (RMSE / target std, averaged over outputs).
"Minimum size" uses the best seed at or below each size (the at-most-P frontier): it is an attained
upper bound on the smallest sufficient MLP for this recipe, not a proof that nothing smaller works.
Post-training uniform quantization of the smallest passing model estimates bits actually used.

Usage:  out/venv/bin/python experiments/reference_ladder.py [--smoke] [--workers 14]
Raw per-run results go to ignored out/ladder_runs/; the summary JSON is written next to this script
and copied into interactive/src/data/reference_ladder.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
import zlib
from functools import lru_cache
from multiprocessing import get_context
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUNS = ROOT / "out" / "ladder_runs"
THRESHOLDS = [0.1, 0.03, 0.01, 0.003]

# ------------------------------------------------------------------ reference functions
G = 9.81


def rk4(f, x, dt, steps):
    for _ in range(steps):
        k1 = f(x); k2 = f(x + 0.5 * dt * k1); k3 = f(x + 0.5 * dt * k2); k4 = f(x + dt * k3)
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x


def pend_f(x, b=0.1):
    th, om = x[:, 0], x[:, 1]
    return np.stack([om, -G * np.sin(th) - b * om], 1)


def dpend_f(x):
    # equal masses and lengths (m=1, l=1); standard double-pendulum equations
    t1, t2, w1, w2 = x[:, 0], x[:, 1], x[:, 2], x[:, 3]
    d = t1 - t2
    den = 3 - np.cos(2 * d)
    a1 = (-3 * G * np.sin(t1) - G * np.sin(t1 - 2 * t2) - 2 * np.sin(d) * (w2 ** 2 + w1 ** 2 * np.cos(d))) / den
    a2 = (2 * np.sin(d) * (2 * w1 ** 2 + 2 * G * np.cos(t1) + w2 ** 2 * np.cos(d))) / den
    return np.stack([w1, w2, a1, a2], 1)


def cart_f(x):
    # Barto et al. cart-pole: m_cart=1, m_pole=0.1, half-length 0.5; force is the 5th column (held)
    mc, mp, l = 1.0, 0.1, 0.5
    th, thd, F = x[:, 2], x[:, 3], x[:, 4]
    s, c = np.sin(th), np.cos(th)
    tmp = (F + mp * l * thd ** 2 * s) / (mc + mp)
    thacc = (G * s - c * tmp) / (l * (4 / 3 - mp * c ** 2 / (mc + mp)))
    xacc = tmp - mp * l * thacc * c / (mc + mp)
    return np.stack([x[:, 1], xacc, thd, thacc, np.zeros_like(F)], 1)


def render(th, n=24):
    ys, xs = np.mgrid[-1:1:complex(n), -1:1:complex(n)].astype(np.float32)
    out = np.empty((len(th), n * n), np.float32)
    for i in range(0, len(th), 4096):  # chunked to bound memory
        t = th[i:i + 4096].astype(np.float32)
        bx, by = 0.75 * np.sin(t), -0.75 * np.cos(t)
        img = np.exp(-(((xs[None] - bx[:, None, None]) ** 2 + (ys[None] - by[:, None, None]) ** 2) / (2 * 0.12 ** 2)))
        out[i:i + 4096] = img.reshape(len(t), -1)
    return out


DT = 0.05


def make_task(name, n, rng):
    """Return X, Y (float32) for a task; Y is the target the network must reproduce."""
    if name in ("pid", "pid_sat"):
        X = rng.uniform(-1, 1, (n, 3))
        u = 2.0 * X[:, 0] + 0.5 * X[:, 1] + 0.1 * X[:, 2]
        Y = np.clip(u, -1, 1) if name == "pid_sat" else u
        return X, Y[:, None]
    if name.startswith("pend") or name == "camera_pend":
        k = int(name.split("_k")[1]) if "_k" in name else 1
        X = np.stack([rng.uniform(-np.pi, np.pi, n), rng.uniform(-6, 6, n)], 1)
        Y = rk4(pend_f, X, DT / 10, 10 * k) - X
        if name == "pend_feat":
            return np.stack([np.sin(X[:, 0]), np.cos(X[:, 0]), X[:, 1]], 1), Y
        if name == "camera_pend":
            prev = rk4(pend_f, X, -DT / 10, 10)  # the frame 50 ms earlier
            return np.concatenate([render(X[:, 0]), render(prev[:, 0])], 1), Y
        return X, Y
    if name.startswith("dpend"):
        k = int(name.split("_k")[1])
        X = np.stack([rng.uniform(-np.pi, np.pi, n), rng.uniform(-np.pi, np.pi, n),
                      rng.uniform(-3, 3, n), rng.uniform(-3, 3, n)], 1)
        return X, rk4(dpend_f, X, DT / 20, 20 * k) - X
    if name == "cartpole":
        X = np.stack([rng.uniform(-2.4, 2.4, n), rng.uniform(-3, 3, n), rng.uniform(-np.pi, np.pi, n),
                      rng.uniform(-6, 6, n), rng.uniform(-10, 10, n)], 1)
        Y = rk4(cart_f, X, 0.002, 10) - X
        return X, Y[:, :4]
    raise ValueError(name)


TASKS = {
    # name: (label, reference constants, rung description)
    "pid": ("PID law", 3, "linear control law"),
    "pid_sat": ("Saturated PID", 4, "piecewise-linear control law"),
    "pend_k1": ("Pendulum, 50 ms step", 3, "nonlinear dynamics, 1 body"),
    "pend_feat": ("Pendulum, 50 ms, sin/cos inputs", 3, "same function, physics-shaped inputs"),
    "cartpole": ("Cart-pole, 20 ms step", 4, "coupled 2-body dynamics with force input"),
    "dpend_k1": ("Double pendulum, 50 ms step", 3, "chaotic 2-body dynamics"),
    "camera_pend": ("Pendulum from two 24×24 frames", 3, "same function, observed through a camera"),
    "pend_k2": ("Pendulum, 100 ms", 3, "regular, longer horizon"),
    "pend_k4": ("Pendulum, 200 ms", 3, "regular, longer horizon"),
    "pend_k8": ("Pendulum, 400 ms", 3, "regular, longer horizon"),
    "pend_k16": ("Pendulum, 800 ms", 3, "regular, longer horizon"),
    "dpend_k2": ("Double pendulum, 100 ms", 3, "chaotic, longer horizon"),
    "dpend_k4": ("Double pendulum, 200 ms", 3, "chaotic, longer horizon"),
    "dpend_k8": ("Double pendulum, 400 ms", 3, "chaotic, longer horizon"),
    "dpend_k16": ("Double pendulum, 800 ms", 3, "chaotic, longer horizon"),
}


@lru_cache(maxsize=2)
def dataset(name, n_train=32768, n_val=2048, n_test=4096):
    # One fixed dataset per task (stable seed); smaller training sets are prefixes of it, so the
    # validation and test sets never change. Normalization uses the full 32k training pool.
    rng = np.random.default_rng(zlib.crc32(name.encode()))
    X, Y = make_task(name, n_train + n_val + n_test, rng)
    X, Y = X.astype(np.float32), Y.astype(np.float32)
    mx, sx = X[:n_train].mean(0), X[:n_train].std(0) + 1e-8
    my, sy = Y[:n_train].mean(0), Y[:n_train].std(0) + 1e-12
    X -= mx; X /= sx
    Y = (Y - my) / sy
    a, b = n_train, n_train + n_val
    return X[:a], Y[:a], X[a:b], Y[a:b], X[b:], Y[b:]


def ftle(system, n=256, T=0.8, seed=0):
    rng = np.random.default_rng(seed)
    if system == "pend":
        X = np.stack([rng.uniform(-np.pi, np.pi, n), rng.uniform(-6, 6, n)], 1); f = pend_f; h = DT / 10
    else:
        X = np.stack([rng.uniform(-np.pi, np.pi, n), rng.uniform(-np.pi, np.pi, n),
                      rng.uniform(-3, 3, n), rng.uniform(-3, 3, n)], 1); f = dpend_f; h = DT / 20
    d = rng.normal(size=X.shape); d /= np.linalg.norm(d, axis=1, keepdims=True); d *= 1e-7
    steps = int(round(T / h))
    a, b = rk4(f, X, h, steps), rk4(f, X + d, h, steps)
    lam = np.log(np.linalg.norm(b - a, axis=1) / 1e-7) / T
    return dict(median=float(np.median(lam)), p90=float(np.percentile(lam, 90)))


# ------------------------------------------------------------------ training
def params_for(d_in, d_out, w):
    return d_in * w + w + w * w + w + w * d_out + d_out


def train_run(job):
    import torch
    torch.set_num_threads(1)
    name, width, n_train, seed, steps, keep = job
    Xtr, Ytr, Xva, Yva, Xte, Yte = dataset(name)
    if n_train:
        Xtr, Ytr = Xtr[:n_train], Ytr[:n_train]
    torch.manual_seed(seed)
    d_in, d_out = Xtr.shape[1], Ytr.shape[1]
    net = torch.nn.Sequential(torch.nn.Linear(d_in, width), torch.nn.SiLU(), torch.nn.Linear(width, width),
                              torch.nn.SiLU(), torch.nn.Linear(width, d_out))
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps, eta_min=1e-5)
    xt, yt = torch.from_numpy(Xtr), torch.from_numpy(Ytr)
    xv, yv = torch.from_numpy(Xva), torch.from_numpy(Yva)
    bs = min(512, len(xt))
    g = torch.Generator().manual_seed(seed)
    best, best_state, t0 = float("inf"), None, time.time()
    for step in range(1, steps + 1):
        idx = torch.randint(len(xt), (bs,), generator=g)
        loss = ((net(xt[idx]) - yt[idx]) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if step % 200 == 0 or step == steps:
            with torch.no_grad():
                v = float(((net(xv) - yv) ** 2).mean())
            if v < best:
                best, best_state = v, {k: t.clone() for k, t in net.state_dict().items()}
    net.load_state_dict(best_state)
    with torch.no_grad():
        nrmse = float(torch.sqrt(((net(torch.from_numpy(Xte)) - torch.from_numpy(Yte)) ** 2).mean(0)).mean())
    out = dict(task=name, width=width, n_train=n_train or len(Xtr), seed=seed, steps=steps,
               params=params_for(d_in, d_out, width), nrmse=nrmse, seconds=round(time.time() - t0, 2))
    if keep:
        out["state"] = {k: t.numpy().tolist() for k, t in best_state.items()}
    return out


def quantized_nrmse(task, state, bits):
    """Uniform symmetric per-tensor quantization of weights and biases; returns test NRMSE."""
    import torch
    Xtr, Ytr, _, _, Xte, Yte = dataset(task)
    layers = sorted({int(k.split('.')[0]) for k in state})
    ws = [np.array(state[f"{i}.{kind}"], dtype=np.float32) for i in layers for kind in ("weight", "bias")]
    q = []
    for w in ws:
        m = np.abs(w).max() or 1.0
        levels = 2 ** (bits - 1) - 1
        q.append(np.round(w / m * levels) / levels * m if bits < 32 else w)
    h = Xte
    for i in range(0, len(q), 2):
        W, b = q[i], q[i + 1]
        h = h @ W.T + b
        if i < len(q) - 2:
            h = h / (1 + np.exp(-h))
    return float(np.sqrt(((h - Yte) ** 2).mean(0)).mean())


def frontier(rows, key):
    """Running best (min NRMSE) at or below each size: the attained at-most-size frontier."""
    pts = sorted(rows, key=lambda r: r[key])
    best, out = float("inf"), []
    for size in sorted({r[key] for r in pts}):
        best = min(best, min(r["nrmse"] for r in pts if r[key] == size))
        out.append((size, best))
    return out


def min_size(front, eps):
    """Smallest size whose frontier NRMSE <= eps, log-interpolated from the last failing size."""
    prev = None
    for size, e in front:
        if e <= eps:
            if prev is None or prev[1] <= eps:
                return float(size)
            (s0, e0) = prev
            t = (math.log(e0) - math.log(eps)) / (math.log(e0) - math.log(e))
            return float(math.exp(math.log(s0) + t * (math.log(size) - math.log(s0))))
        prev = (size, e)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    RUNS.mkdir(parents=True, exist_ok=True)
    if args.smoke:
        tasks, widths, sizes, seeds_c, seeds_d, steps = ["pid", "pend_k1"], [4, 32], [256, 2048], [0], [0], 400
    else:
        tasks = list(TASKS)
        widths, sizes = [2, 4, 8, 16, 32, 64, 128, 256], [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
        seeds_c, seeds_d, steps = [0, 1, 2], [0, 1], 4000
    jobs = [(t, w, 0, s, steps, True) for t in tasks for w in widths for s in seeds_c]
    jobs += [(t, 128, n, s, steps, False) for t in tasks for n in sizes for s in seeds_d]
    jobs.sort(key=lambda j: -(j[1] * j[1] + (1152 * j[1] if j[0] == "camera_pend" else 0)))  # big first
    t0 = time.time()
    results = []
    with get_context("fork").Pool(args.workers) as pool:
        for i, r in enumerate(pool.imap_unordered(train_run, jobs), 1):
            results.append(r)
            if i % 25 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)} runs, {time.time() - t0:.0f}s", flush=True)
    cap = [r for r in results if "state" in r]
    dat = [r for r in results if "state" not in r]
    (RUNS / ("smoke.json" if args.smoke else "runs.json")).write_text(
        json.dumps([{k: v for k, v in r.items() if k != "state"} for r in results]))

    summary = dict(generated=time.strftime("%Y-%m-%d %H:%M"), steps=steps, widths=widths, sizes=sizes,
                   thresholds=THRESHOLDS, cpu_seconds=round(sum(r["seconds"] for r in results)),
                   wall_seconds=round(time.time() - t0), ftle={}, tasks=[])
    if not args.smoke:
        summary["ftle"] = {"pendulum": ftle("pend"), "double_pendulum": ftle("dpend")}
    for t in tasks:
        label, consts, rung = TASKS[t]
        c = [r for r in cap if r["task"] == t]
        d = [r for r in dat if r["task"] == t]
        cf, df = frontier(c, "params"), frontier(d, "n_train")
        pmin = {str(e): min_size(cf, e) for e in THRESHOLDS}
        dmin = {str(e): min_size(df, e) for e in THRESHOLDS}
        # bits actually used: quantize the best model at the smallest width reaching 1% (or the widest)
        passing = sorted({r["width"] for r in c if r["nrmse"] <= 0.01})
        w_q = passing[0] if passing else max(widths)
        best = min((r for r in c if r["width"] == w_q), key=lambda r: r["nrmse"])
        qcurve = {b: quantized_nrmse(t, best["state"], b) for b in [16, 12, 10, 8, 6, 5, 4, 3, 2]}
        target = max(0.01, best["nrmse"] * 1.25)
        bmin = min([b for b, e in qcurve.items() if e <= target], default=None)
        summary["tasks"].append(dict(
            id=t, label=label, reference_constants=consts, rung=rung,
            d_in=int(dataset(t)[0].shape[1]), d_out=int(dataset(t)[1].shape[1]),
            capacity=[dict(params=p, nrmse=e) for p, e in cf],
            capacity_all=[dict(params=r["params"], seed=r["seed"], nrmse=r["nrmse"]) for r in c],
            data=[dict(n=n, nrmse=e) for n, e in df],
            p_min=pmin, d_min=dmin,
            quant=dict(width=w_q, params=best["params"], float_nrmse=best["nrmse"],
                       curve={str(b): e for b, e in qcurve.items()}, b_min=bmin,
                       bits_used=(best["params"] * bmin) if bmin else None)))
    name = "reference_ladder_smoke.json" if args.smoke else "reference_ladder_results.json"
    (HERE / name).write_text(json.dumps(summary, indent=1))
    if not args.smoke:
        (ROOT / "interactive/src/data/reference_ladder.json").write_text(json.dumps(summary))
    print(f"done in {time.time() - t0:.0f}s wall, {summary['cpu_seconds']} CPU-s -> {name}")


if __name__ == "__main__":
    main()
