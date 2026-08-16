from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from manim import Mobject


@dataclass(frozen=True)
class Bounds:
    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom


def bounds(mobject: Mobject) -> Bounds:
    return Bounds(
        left=float(mobject.get_left()[0]),
        right=float(mobject.get_right()[0]),
        bottom=float(mobject.get_bottom()[1]),
        top=float(mobject.get_top()[1]),
    )


def assert_text_fits(text: Mobject, container: Mobject, *, name: str = "text", pad: float = 0.08) -> None:
    text_bounds = bounds(text)
    container_bounds = bounds(container)
    max_width = max(0.0, container_bounds.width - pad * 2)
    max_height = max(0.0, container_bounds.height - pad * 2)
    if text_bounds.width > max_width or text_bounds.height > max_height:
        raise ValueError(
            f"{name} does not fit container: "
            f"text={text_bounds.width:.2f}x{text_bounds.height:.2f} "
            f"container={container_bounds.width:.2f}x{container_bounds.height:.2f} pad={pad:.2f}"
        )


def assert_in_safe_area(
    mobject: Mobject,
    *,
    name: str = "mobject",
    x_max: float = 6.85,
    y_max: float = 3.72,
    pad: float = 0.0,
) -> None:
    b = bounds(mobject)
    if b.left < -x_max + pad or b.right > x_max - pad or b.bottom < -y_max + pad or b.top > y_max - pad:
        raise ValueError(
            f"{name} outside safe area: "
            f"x=({b.left:.2f},{b.right:.2f}) y=({b.bottom:.2f},{b.top:.2f}) "
            f"safe=(+/-{x_max:.2f}, +/-{y_max:.2f})"
        )


def assert_no_overlap(a: Mobject, b: Mobject, *, name: str = "mobjects", tolerance: float = 0.05) -> None:
    ba = bounds(a)
    bb = bounds(b)
    separated = (
        ba.right <= bb.left + tolerance
        or bb.right <= ba.left + tolerance
        or ba.top <= bb.bottom + tolerance
        or bb.top <= ba.bottom + tolerance
    )
    if not separated:
        raise ValueError(
            f"{name} overlap: "
            f"a=({ba.left:.2f},{ba.right:.2f},{ba.bottom:.2f},{ba.top:.2f}) "
            f"b=({bb.left:.2f},{bb.right:.2f},{bb.bottom:.2f},{bb.top:.2f})"
        )


def fit_text_to_width(text: Mobject, max_width: float, *, min_scale: float = 0.72) -> Mobject:
    if text.width <= max_width:
        return text
    scale = max(min_scale, max_width / max(0.001, text.width))
    text.scale(scale)
    return text


def assert_no_pairwise_overlap(mobjects: Iterable[Mobject], *, name: str = "mobjects", tolerance: float = 0.05) -> None:
    items = list(mobjects)
    for i, first in enumerate(items):
        for second in items[i + 1:]:
            assert_no_overlap(first, second, name=name, tolerance=tolerance)
