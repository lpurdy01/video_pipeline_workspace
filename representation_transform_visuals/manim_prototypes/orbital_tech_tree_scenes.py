from __future__ import annotations

import numpy as np
from manim import *

from orbital_tech_tree_data import STATE_CAMERA
from orbital_tech_tree_map import OrbitalTechTreeMap
from visual_style import BG


class OrbitalTechTreeProgressivePrototype(MovingCameraScene):
    """Motion test for the tech tree as a progressive-reveal story spine."""

    def setup(self):
        self.camera.background_color = BG

    def move_to_state(self, tree: OrbitalTechTreeMap, state: str, run_time: float = 2.0):
        cam = STATE_CAMERA[state]
        center = np.array([cam["center"][0], cam["center"][1], 0.0])
        width = config.frame_width * cam["scale"]
        self.play(
            self.camera.frame.animate.move_to(center).set(width=width),
            tree.fog_drift_animation(run_time=run_time * 0.62),
            run_time=run_time * 0.62,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(tree.apply_state(state, animate=True, run_time=0.42), run_time=0.42)

    def construct(self):
        tree = OrbitalTechTreeMap(self)
        tree.add_to_scene()

        self.camera.frame.set(width=config.frame_width * STATE_CAMERA["opening_glimpse"]["scale"])
        self.camera.frame.move_to(np.array([0.05, 0.08, 0.0]))

        states = [
            "opening_glimpse",
            "classical_foundation",
            "modern_region",
            "convergence_pullback",
            "final_reveal",
        ]

        self.play(tree.fog_drift_animation(run_time=2.0), run_time=2.0)

        for state in states[1:]:
            self.move_to_state(tree, state, run_time=2.1)
            self.play(tree.fog_drift_animation(run_time=1.2), run_time=1.2)

        self.wait(0.8)


class OrbitalTechTreeFinalRevealStill(Scene):
    """Static final-reveal frame for quick visual review."""

    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        tree = OrbitalTechTreeMap(self)
        tree.apply_state("final_reveal", animate=False)
        tree.add_to_scene()
