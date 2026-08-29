"""
Does the geometry recorder see a 3D scene the way the viewer does?

World coordinates are meaningless for layout in 3D: two nodes far apart in z can
sit on top of each other on screen, and a node behind the camera has a perfectly
reasonable-looking x. This plants exactly that — nodes that do not overlap in
world space but do overlap once projected — and asserts the checks catch it.

Without this, a 3D scene renders with no effective checking at all.
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from verification_compiler_video.pipeline import qa, style


class Projected3D(qa.QASceneMixin, ThreeDScene):
    def construct(self):
        self.camera.background_color = style.BG
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # Far apart in z, stacked on screen once the camera looks down the axis.
        a = style.node("code", "FRONT", size=1.6).move_to(np.array([0.0, 0.0, 0.0]))
        b = style.node("test", "BEHIND", size=1.6).move_to(np.array([0.0, 0.0, -3.0]))
        self.add(a, b)
        self.wait(1.5)

        # Now swing the camera so they separate on screen.
        self.move_camera(phi=70 * DEGREES, theta=-60 * DEGREES, run_time=1.5)
        self.wait(1.0)


def main() -> int:
    geo = Path("out/qa/Projected3D.geometry.json")
    if not geo.exists():
        print(f"render first:\n  manim -ql --disable_caching {__file__} Projected3D")
        return 2
    import json
    data = json.loads(geo.read_text())
    first = sorted(data["samples"], key=lambda s: s["t"])[0]
    nodes = [b for b in first["boxes"] if b["kind"] == "node"]
    if len(nodes) < 2:
        print("FAIL — nodes were not recorded at all")
        return 1
    frac = qa._overlap_fraction(tuple(nodes[0]["box"]), tuple(nodes[1]["box"]))
    print(f"head-on: two nodes 3.0 apart in z overlap {frac:.0%} on screen")

    last = sorted(data["samples"], key=lambda s: s["t"])[-1]
    lnodes = [b for b in last["boxes"] if b["kind"] == "node"]
    frac2 = qa._overlap_fraction(tuple(lnodes[0]["box"]), tuple(lnodes[1]["box"]))
    print(f"after camera move: they overlap {frac2:.0%}")

    if frac < 0.5:
        print("\nFAIL — projection is not being applied; world coords were recorded")
        return 1
    if frac2 > 0.4:
        print("\nFAIL — the camera move had no effect on recorded geometry")
        return 1
    print("\nSELFTEST PASS — recorded geometry follows the camera")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
