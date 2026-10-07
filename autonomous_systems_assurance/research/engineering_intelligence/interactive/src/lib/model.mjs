/** An explicitly uncalibrated, task-conditional hypothesis model. */
export const defaults = Object.freeze({
  width: 640, height: 360, frames: 2, patch: 16, feature: 16,
  context: 4096, factors: 32, depth: 4, reuse: 16, novelty: 0.15,
  novelExamples: 50000, tailExamples: 1000, output: 1,
  selectedM: 100, anchorM: 100, anchorOrd: 0.82, anchorTail: 0.45,
  targetOrd: 0.90, targetTail: 0.80, uncertainty: 3, taskBits: 0,
  bits: 16, kvKB: 16, memoryGB: 8, tflops: 40, bandwidthGBs: 900, deadlineMs: 50,
});

const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const million = 1e6;
const baseline = defaults;

export const presets = Object.freeze({
  road: { ...defaults },
  compact: { ...defaults, width: 128, height: 128, frames: 1, patch: 8, feature: 8, context: 1024, factors: 8, depth: 2, reuse: 30, novelty: 0.05, selectedM: 10, targetTail: 0.70, deadlineMs: 20 },
  dense: { ...defaults, width: 1280, height: 720, frames: 4, patch: 16, feature: 12, context: 8192, factors: 96, depth: 7, reuse: 6, novelty: 0.30, tailExamples: 300, selectedM: 1000, targetTail: 0.75, deadlineMs: 100 },
});

function caps(s) {
  const tokens = s.frames * Math.ceil(s.width / s.patch) * Math.ceil(s.height / s.patch);
  const processed = Math.min(tokens, s.context);
  // Hypothesis: lossy pooled patches can suppress features smaller than a patch.
  // This is deliberately not a theorem about all patch embeddings.
  const detail = Math.pow(Math.min(1, s.feature / s.patch), 0.75);
  const history = Math.sqrt(Math.min(1, s.context / tokens));
  const observation = 0.995 * detail * history;
  return {
    tokens, processed, detail, history, observation,
    ordinary: observation * (1 - Math.exp(-s.novelExamples / 10000)),
    tail: observation * (1 - Math.exp(-s.tailExamples / 300)),
  };
}

function inverseSaturation(coverage, ceiling, alpha) {
  const ratio = clamp(coverage / ceiling, 1e-9, 0.999999);
  return Math.pow(-Math.log(1 - ratio), 1 / alpha);
}

function structure(s) {
  return Math.pow(s.factors / baseline.factors, 0.7)
    * Math.pow((1 + s.depth) / (1 + baseline.depth), 0.8)
    * Math.pow((s.reuse + 2) / (baseline.reuse + 2), -0.35)
    * Math.pow((s.novelty + 0.1) / (baseline.novelty + 0.1), 0.25);
}

export function derive(input = {}) {
  const s = { ...defaults, ...input };
  const c = caps(s);
  const ref = caps(defaults);
  const alphaOrd = 0.65;
  const alphaTail = 0.50;
  const refP50Ord = s.anchorM * million / inverseSaturation(s.anchorOrd, ref.ordinary, alphaOrd);
  const refP50Tail = s.anchorM * million / inverseSaturation(s.anchorTail, ref.tail, alphaTail);
  const scale = structure(s);
  const p50Ord = refP50Ord * scale;
  const p50Tail = refP50Tail * scale
    * Math.pow((s.novelty + 0.1) / (baseline.novelty + 0.1), 0.6)
    * Math.pow(s.tailExamples / baseline.tailExamples, -0.25);
  const ordinaryAt = p => c.ordinary * (1 - Math.exp(-Math.pow(p / p50Ord, alphaOrd)));
  const tailAt = p => c.tail * (1 - Math.exp(-Math.pow(p / p50Tail, alphaTail)));
  const inverse = (target, ceiling, p50, alpha) => target >= ceiling ? null : p50 * inverseSaturation(target, ceiling, alpha);
  const reqOrd = inverse(s.targetOrd, c.ordinary, p50Ord, alphaOrd);
  const reqTail = inverse(s.targetTail, c.tail, p50Tail, alphaTail);
  const required = reqOrd === null || reqTail === null ? null : Math.max(reqOrd, reqTail);
  const kvBytes = s.kvKB * 1024 * c.processed;
  const weightBytesAt = p => p * s.bits / 8;
  const memoryAt = p => weightBytesAt(p) + kvBytes;
  // Dense-transformer work scenario: all P weights active per processed token.
  const flopsAt = p => 2 * p * (c.processed + s.output);
  // Explicit single-request traffic scenario: one weight read in prefill and
  // one per output step, plus a full KV read per output step.
  const trafficAt = p => weightBytesAt(p) * (1 + s.output) + kvBytes * s.output;
  const computeMsAt = p => flopsAt(p) / (s.tflops * 1e12) * 1000;
  const bandwidthMsAt = p => trafficAt(p) / (s.bandwidthGBs * 1e9) * 1000;
  const latencyAt = p => Math.max(computeMsAt(p), bandwidthMsAt(p));
  const pMaxMemory = Math.max(0, (s.memoryGB * 1e9 - kvBytes) * 8 / s.bits);
  const pMaxCompute = s.deadlineMs / 1000 * s.tflops * 1e12 / (2 * (c.processed + s.output));
  const pMaxBandwidth = Math.max(0, (s.deadlineMs / 1000 * s.bandwidthGBs * 1e9 - kvBytes * s.output) * 8 / (s.bits * (1 + s.output)));
  const pMax = Math.min(pMaxMemory, pMaxCompute, pMaxBandwidth);
  const selected = s.selectedM * million;
  return {
    s, ...c, p50Ord, p50Tail, ordinaryAt, tailAt, reqOrd, reqTail, required,
    selected, memoryAt, flopsAt, trafficAt, computeMsAt, bandwidthMsAt, latencyAt,
    pMaxMemory, pMaxCompute, pMaxBandwidth, pMax,
    uncertaintyLow: required === null ? null : required / s.uncertainty,
    uncertaintyHigh: required === null ? null : required * s.uncertainty,
    countingFloor: Math.ceil(s.taskBits / s.bits),
    limitingResource: pMax === pMaxMemory ? 'memory' : pMax === pMaxCompute ? 'compute' : 'bandwidth',
  };
}
