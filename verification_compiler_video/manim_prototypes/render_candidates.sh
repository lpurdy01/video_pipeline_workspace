#!/usr/bin/env bash
# Render the B and C candidate sets at preview quality for selection review.
set -uo pipefail
cd "$(dirname "$0")"

render() {
  local file="$1" scene="$2"
  if manim -ql --format=mp4 --disable_caching "$file" "$scene" >"/tmp/manim_${scene}.log" 2>&1; then
    echo "OK   $scene"
  else
    echo "FAIL $scene  (see /tmp/manim_${scene}.log)"
  fi
}
export -f render

B=(B01RateDivergence B02TwoColumnLedger B03ReverseAudit B04ChainsBecomeGraph B05TraversalWalk
   B06FoldPackage B07ReviewerSwap B08VersionLedger B09ReadinessTrend B10TheLoop)
C=(C01ReviewQueue C02TranscriptVsRecord C03TraceTable C04TableLiftsToGraph C05TwoCompilers
   C06VQPDocument C07IdenticalSchema C08HashMismatch C09CIOutput C10DecisionSurface)

printf '%s\n' "${B[@]}" | xargs -P 5 -I{} bash -c 'render candidates_b.py {}'
printf '%s\n' "${C[@]}" | xargs -P 5 -I{} bash -c 'render candidates_c.py {}'
