/**
 * Intelligence-budget hypothesis (see ../../../intelligence_budget.md).
 * Everything is measured in bits. The task is one curve K(eps); storage, hardware time and
 * training data each supply a bit budget; the smallest budget sets the reducible error.
 * Presets are ILLUSTRATIVE anchors, not measurements of any product.
 */

// Reducible error supplied `bits` of task description. Truncated-Zipf residual:
// eps(b) = eps0 * [ (b/K0)^-alpha - (Kodd/K0)^-alpha ]_+  (reaches 0 when the ODD spectrum is exhausted)
export function epsFromBits(bits, t) {
  if (!(bits > 0)) return Infinity;
  const tail = Math.pow(t.Kodd / t.K0, -t.alpha);
  return Math.max(0, t.eps0 * (Math.pow(bits / t.K0, -t.alpha) - tail));
}

// Bits needed for reducible error eps (inverse of epsFromBits); null if eps below what the curve allows.
export function bitsForEps(eps, t) {
  if (eps <= 0) return t.Kodd;
  const tail = Math.pow(t.Kodd / t.K0, -t.alpha);
  const x = eps / t.eps0 + tail;
  return Math.min(t.Kodd, t.K0 * Math.pow(x, -1 / t.alpha));
}

const LN = Math.log;
const db = x => 10 * Math.log10(x);

export const presets = Object.freeze({
  cartpole: {
    label: 'Cart-pole balance (state feedback)',
    note: 'K anchored to the measured d_int90 = 4 (Li et al. 2018) × 32 bits. Sensor: full state, declared adequate.',
    K0: 128, eps0: 0.1, alpha: 1.0, Kodd: 256, rho: 1, target: 0.05, obsFloor: 0.0,
    sensor: 'declared', obsRatio: 5,
    streams: 1, width: 1, height: 1, patch: 1, frames: 1, fovDeg: 60, targetM: 1, rangeM: 1, nReq: 2,
    kappa: 2, bits: 32, topsEff: 0.0001, bwGBs: 0.1, memGB: 0.0005, deadlineMs: 10, Z: 0, passMs: 0.05, tokensOverride: 1,
    D: 5000, sEff: 1, eta: 0.1, pRare: 0.1, tau: 100, examplesPerHour: 3600,
    n: 30000, pTarget: 1e-4, conf: 0.95, modelP: 64,
  },
  acas: {
    label: 'ACAS Xu advisory networks',
    note: 'K0 ≈ 2 bits/param × 0.5M params (Julian et al.). α, ODD cap and error scale are illustrative.',
    K0: 1e6, eps0: 0.01, alpha: 0.5, Kodd: 4e6, rho: 1, target: 0.005, obsFloor: 0.0,
    sensor: 'declared', obsRatio: 1.5,
    streams: 1, width: 1, height: 1, patch: 1, frames: 1, fovDeg: 60, targetM: 1, rangeM: 1, nReq: 2,
    kappa: 2, bits: 32, topsEff: 0.001, bwGBs: 1, memGB: 0.1, deadlineMs: 1000, Z: 0, passMs: 1, tokensOverride: 1,
    D: 1.2e8, sEff: 2.3, eta: 0.01, pRare: 1e-4, tau: 300, examplesPerHour: 1e6,
    n: 1.5e6, pTarget: 1e-5, conf: 0.95, modelP: 495000,
  },
  face: {
    label: 'Face verification on a phone',
    note: 'K0 ≈ 2 bits/param × ~1M params at 1−TAR ≈ 7% (MobileFaceNet @ FAR 1e-6). Pixel need = Johnson identification ideal (6.4 cycles). Tokens = effective: 221M multiply-adds ÷ P, since a CNN is not a dense transformer.',
    K0: 2e6, eps0: 0.074, alpha: 0.25, Kodd: 1e12, rho: 1, target: 0.084, obsFloor: 0.01,
    sensor: 'camera', obsRatio: 1,
    streams: 1, width: 1920, height: 1080, patch: 16, frames: 1, fovDeg: 70, targetM: 0.15, rangeM: 1.5, nReq: 12.8,
    kappa: 2, bits: 8, topsEff: 10, bwGBs: 50, memGB: 4, deadlineMs: 100, Z: 0, passMs: 2, tokensOverride: 221,
    D: 5e6, sEff: 20, eta: 0.05, pRare: 1e-3, tau: 300, examplesPerHour: 200,
    n: 1e6, pTarget: 1e-5, conf: 0.95, modelP: 1e6,
  },
  imagenet: {
    label: 'ImageNet-class classifier on a Jetson-class module',
    note: 'K0 = 2 bits/param × 9.1M (smallest listed ≥80% model); α ≈ 0.2 fitted to the best-listed TorchVision frontier across recipes. Data line: 1.28M labels × log₂1000 ≈ 12.8 Mbit, the most label information ImageNet-1k can deliver.',
    K0: 1.82e7, eps0: 0.20, alpha: 0.2, Kodd: 1e13, rho: 1, target: 0.22, obsFloor: 0.02,
    sensor: 'declared', obsRatio: 1.2,
    streams: 1, width: 224, height: 224, patch: 16, frames: 1, fovDeg: 60, targetM: 1, rangeM: 1, nReq: 2,
    kappa: 2, bits: 8, topsEff: 100, bwGBs: 204.8, memGB: 64, deadlineMs: 33, Z: 0, passMs: 1, tokensOverride: 0,
    D: 1.28e6, sEff: 9.97, eta: 1, pRare: 1e-3, tau: 300, examplesPerHour: 0,
    n: 50000, pTarget: 1e-3, conf: 0.95, modelP: 9.1e6,
  },
  daa: {
    label: 'Airborne camera detect-and-avoid (NASA geometry)',
    note: 'Camera and SR22 size from NASA flight test; pixel need 11 = what that system needed. 3.1 km ≈ 30 s at 200 kt closure. K0 = 2 × YOLOv8s-scale (illustrative).',
    K0: 2.24e7, eps0: 0.13, alpha: 0.3, Kodd: 1e11, rho: 1, target: 0.15, obsFloor: 0.02,
    sensor: 'camera', obsRatio: 1,
    streams: 1, width: 3840, height: 2160, patch: 16, frames: 1, fovDeg: 41, targetM: 5.64, rangeM: 3100, nReq: 11,
    kappa: 2, bits: 8, topsEff: 50, bwGBs: 102.4, memGB: 16, deadlineMs: 100, Z: 0, passMs: 2, tokensOverride: 0,
    D: 1e6, sEff: 30, eta: 1, pRare: 1e-3, tau: 300, examplesPerHour: 50,
    n: 3000, pTarget: 1e-3, conf: 0.95, modelP: 11.2e6,
  },
  drive: {
    label: 'Vision-to-control at 36 Hz (hypothetical car)',
    note: 'Entirely hypothetical task curve. Hardware: DRIVE-Orin-class effective rates. Tokens: assumes a learned video tokenizer compresses 8 cameras to ~2k tokens per decision (raw 16-px patches would be 38,400). Supervision 0.5 bit/example = action-only; try 10⁴ for dense proxy tasks. Target: 0.5 m object at 80 m. Collection hours are single-vehicle hours of useful examples: divide by fleet size (Duan, CVPR 2026: Tesla’s fleet drives about 500 years per day).',
    K0: 1e9, eps0: 0.05, alpha: 0.3, Kodd: 5e10, rho: 1, target: 0.03, obsFloor: 0.005,
    sensor: 'camera', obsRatio: 1,
    streams: 8, width: 1280, height: 960, patch: 16, frames: 1, fovDeg: 60, targetM: 0.5, rangeM: 80, nReq: 6,
    kappa: 2, bits: 8, topsEff: 100, bwGBs: 200, memGB: 32, deadlineMs: 27.8, Z: 0, passMs: 3, tokensOverride: 2048,
    D: 1e9, sEff: 0.5, eta: 0.1, pRare: 1e-6, tau: 300, examplesPerHour: 360,
    n: 3e6, pTarget: 1e-6, conf: 0.95, modelP: 5e8,
  },
});

export function evaluate(s) {
  const t = { K0: s.K0, eps0: s.eps0, alpha: s.alpha, Kodd: s.Kodd };
  // ---- Tokens and timing
  const T = s.tokensOverride > 0 ? s.tokensOverride
    : s.streams * s.frames * Math.ceil(s.width / s.patch) * Math.ceil(s.height / s.patch);
  const C = s.topsEff * 1e12;            // effective ops/s
  const B = s.bwGBs * 1e9;               // effective bytes/s
  const L = s.deadlineMs / 1000;
  const serial = (1 + s.Z) * s.passMs / 1000;
  const perParamCompute = 2 * (T + s.Z) / C;             // s per parameter
  const perParamMemory = (1 + s.Z) * (s.bits / 8) / B;   // s per parameter (weights re-read per pass)
  const budget = Math.max(0, L - serial);
  const pMaxCompute = budget / perParamCompute;
  const pMaxBandwidth = budget / perParamMemory;
  const pMaxMemory = s.memGB * 1e9 * 8 / s.bits * 0.7;   // 30% reserved for activations/KV/runtime (assumption)
  const pMaxOpt = Math.min(pMaxCompute, pMaxBandwidth, pMaxMemory);
  const pMaxPess = Math.min(budget / (perParamCompute + perParamMemory), pMaxMemory);
  const binding = pMaxOpt === pMaxMemory ? 'memory' : pMaxOpt === pMaxCompute ? 'compute' : 'bandwidth';
  const tAt = P => ({ opt: Math.max(P * perParamCompute, P * perParamMemory) + serial,
                      pess: P * (perParamCompute + perParamMemory) + serial });
  // ---- Observation
  const ifov = (s.fovDeg * Math.PI / 180) / s.width;
  const pxOnTarget = s.targetM / (s.rangeM * ifov);
  const piObs = s.sensor === 'camera' ? pxOnTarget / s.nReq : s.obsRatio;
  const subPatch = s.sensor === 'camera' && pxOnTarget < s.patch;
  // ---- Task bits and capacity
  const reducibleTarget = Math.max(0, s.target - s.obsFloor);
  const Kneed = s.rho * bitsForEps(reducibleTarget, t);
  const pMin = Kneed / s.kappa;
  const bitsStore = s.kappa * s.modelP / s.rho;
  const bitsStoreMax = s.kappa * pMaxOpt / s.rho;
  const bitsTaught = s.eta * s.sEff * s.D / s.rho;
  const piCap = s.kappa * s.modelP / Kneed;
  const piDataBits = s.eta * s.sEff * s.D / Kneed;
  const piTail = s.D * s.pRare / s.tau;
  const piData = Math.min(piDataBits, piTail);
  // Data required (hypothesis): enough examples to deliver the task bits AND enough exposures of the
  // rarest needed skill. Hours use the rate of useful, independent examples per hour of collection.
  const dBits = Kneed / (s.eta * s.sEff);
  const dTail = s.tau / s.pRare;
  const dReq = Math.max(dBits, dTail);
  const dBinding = dBits >= dTail ? 'task bits' : 'rarest skill';
  const hoursReq = s.examplesPerHour > 0 ? dReq / s.examplesPerHour : null;
  const tModel = tAt(s.modelP);
  const piRt = L / tModel.opt;
  const piRtPess = L / tModel.pess;
  const piEv = s.n * s.pTarget / LN(1 / (1 - s.conf));
  const obsLimited = piObs < 1;
  const epsAt = bits => s.obsFloor * (obsLimited ? 1 / Math.max(piObs, 1e-3) : 1) + epsFromBits(bits, t);
  const epsModel = epsAt(Math.min(bitsStore, bitsTaught));
  const epsBest = epsAt(Math.min(bitsStoreMax, bitsTaught));
  const marginDb = db(s.kappa * pMaxOpt / Kneed);
  const ledger = [
    { label: 'κ bits/param', db: db(s.kappa) },
    { label: 'P_max (hardware, L)', db: db(pMaxOpt) },
    { label: 'ρ_A mismatch', db: -db(s.rho) },
    { label: 'task bits K*(ε)', db: -db(Kneed / s.rho) },
  ];
  return {
    T, pMaxCompute, pMaxBandwidth, pMaxMemory, pMaxOpt, pMaxPess, binding, tModel,
    ifov, pxOnTarget, piObs, subPatch, Kneed, pMin, bitsStore, bitsStoreMax, bitsTaught,
    piCap, piData, piDataBits, piTail, dBits, dTail, dReq, dBinding, hoursReq, piRt, piRtPess, piEv, epsModel, epsBest, marginDb, ledger,
    curve: P => epsAt(Math.min(s.kappa * P / s.rho, bitsTaught)),
    curveNoData: P => epsAt(s.kappa * P / s.rho),
  };
}

export const fmt = (x, d = 2) => {
  if (x === null || x === undefined || !isFinite(x)) return '—';
  const a = Math.abs(x);
  if (a === 0) return '0';
  if (a >= 1e12) return (x / 1e12).toFixed(d) + 'T';
  if (a >= 1e9) return (x / 1e9).toFixed(d) + 'B';
  if (a >= 1e6) return (x / 1e6).toFixed(d) + 'M';
  if (a >= 1e3) return (x / 1e3).toFixed(d) + 'k';
  if (a >= 0.01) return x.toFixed(d);
  return x.toExponential(1);
};
