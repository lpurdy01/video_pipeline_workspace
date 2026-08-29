"""
Beats: the unit of visual change.

The brief is that almost every line of narration should change the picture. That
is only tractable if a "change" is a first-class object, so this module makes one.

A Beat binds a fragment of narration to a visual change:

    Beat("a chat transcript is not evidence", show_transcript_fails)

The scene does not decide *when* that happens. The timing table does, and the
timing table comes from the audio. A beat that runs long is compressed to fit its
window rather than pushing everything after it out of sync — which is the failure
that made video 1 need repeated retiming passes.

Ownership is tracked. A beat says what it introduces and what it retires, and the
stage removes the retired things itself. That kills two recurring Manim bugs at
once: fading out something already gone (which re-adds it at full opacity and
flashes it into frame) and leaving stale mobjects on stage under the next beat.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from manim import *

from . import stage, style, timing
from .qa import QASceneMixin, _is_text


# The final cut is exported sped up, so on-screen holds must be judged at that
# speed. A caption that reads fine at 1.0x is a flash at 1.25x.
EXPORT_SPEED = 1.25
MIN_CAPTION_HOLD = 3.0 * EXPORT_SPEED  # seconds of 1.0x time

# Longer than this with a frozen frame and the viewer notices. The gate's
# dead_air threshold is 5.0s; flagging at 3.5s means a beat gets reported
# while it is merely slack, before it is a violation.
IDLE_LIMIT = 3.5


@dataclass
class Beat:
    """One visual change, cued to a line of narration."""

    anchor: str
    build: Callable[["BeatContext"], None]
    lead: float = 0.0          # start this many seconds early (for slow reveals)
    note: str = ""             # storyboard intent, surfaced in review

    # resolved at run time
    start: float = field(default=0.0, init=False)
    window: float = field(default=0.0, init=False)


class BeatContext:
    """What a beat is handed. The only sanctioned way to touch the stage."""

    def __init__(self, scene: "BeatScene", beat: Beat):
        self.scene = scene
        self.beat = beat

    # -- time -------------------------------------------------------------
    @property
    def window(self) -> float:
        """Seconds available before the next beat is due."""
        return self.beat.window

    def budget(self, *run_times: float) -> list[float]:
        """
        Scale a set of intended run times to fit the window.

        Never stretches — a beat that finishes early simply holds. This is what
        keeps a long beat from shoving every later cue out of sync.
        """
        total = sum(run_times)
        usable = max(self.window - 0.12, 0.2)
        if total <= usable:
            return list(run_times)
        k = usable / total
        return [max(rt * k, 0.08) for rt in run_times]

    # -- stage ------------------------------------------------------------
    def show(self, *mobs: Mobject, tag: str | None = None, anim=None, run_time: float = 0.6,
             nudge: bool = True):
        """
        Introduce mobjects, optionally under a tag so a later beat can retire them.

        A single mobject is owned as itself rather than wrapped in a VGroup, so
        `self._owned[tag]` is the thing you passed in. Wrapping made every index
        into an owned group off by one level, which is a bug that only shows up
        at render time.

        A bare label is nudged clear of text already on stage before it appears.
        Beats are written independently and cannot see each other's placements,
        so "below this box" in two different beats resolves to the same strip of
        screen and the two labels land a tenth of a unit apart — legible alone,
        a smudge together. Pass nudge=False for a label whose exact position is
        the point.
        """
        group = mobs[0] if len(mobs) == 1 else VGroup(*mobs)
        if nudge:
            self._nudge_clear(group)
        if tag:
            self.scene._own(tag, group)
        rt = self.budget(run_time)[0]
        self.scene.play(anim(group) if anim else FadeIn(group), run_time=rt)
        return group

    def _nudge_clear(self, group: Mobject) -> None:
        """
        Give a standalone label air, against whatever text is already on stage.

        Only standalone text moves. A node carries its label inside a shape and
        its position is a compositional decision, so shoving it sideways to gain
        a tenth of a unit would be the pipeline overruling the storyboard.
        """
        texts = [m for m in group.get_family() if _is_text(m)]
        if not texts:
            return
        # A Text is a container of glyph paths; the glyphs hold the points, not
        # the Text. So "is this group nothing but text?" has to be asked of the
        # glyphs, not of the mobjects that happen to be Text instances.
        glyphs = {id(g) for t in texts for g in t.get_family()}
        points = [m for m in group.get_family() if len(m.get_all_points())]
        if not points or any(id(m) not in glyphs for m in points):
            return
        if any(getattr(t, "qa_allow_overlap", None) for t in texts):
            return

        others, shapes = [], []
        for top in self.scene.mobjects:
            for m in top.get_family():
                if id(m) in glyphs or getattr(m, "qa_ignore", False):
                    continue
                if not len(m.get_all_points()):
                    continue
                if _is_text(m):
                    lit = max((float(getattr(g, "fill_opacity", 0) or 0)
                               for g in m.get_family()), default=0.0)
                    if lit > 0.35:
                        others.append(m)
                elif getattr(m, "qa_role", None) == "node" or (
                        not m.submobjects and getattr(m, "qa_role", None) is None):
                    # A drawn shape. A standalone label has to clear these too:
                    # a caption whose box straddles a card's edge gets that edge
                    # drawn through its letters, whichever way the layering
                    # falls, and that was the single most common defect in the
                    # last review — "coordination", "reviewable", "traversal",
                    # "reviewer", "version mismatch", all the same story.
                    shapes.append(m)

        moved = 0.0
        if others:
            moved += stage.clear_of(group, others)
        if shapes:
            # Best-effort, and never fatal. Clearing text of text is a tight,
            # reliable case worth failing the build over; clearing a label of a
            # half-metre-wide card is a heuristic, and a heuristic that cannot
            # find room should hand the decision back rather than stop the
            # render. The gate still reports it if it really is a defect.
            home = group.get_center().copy()
            try:
                # A bigger allowance than for text: getting clear of a card means
                # crossing its whole height, not a tenth of a unit of air.
                moved += stage.clear_of(group, shapes, limit=1.8, crossing_only=True)
            except ValueError as exc:
                group.move_to(home)
                self.scene._nudges.append(
                    (self.beat.anchor[:44],
                     f"{stage._describe(group)} left where it was: {exc.args[0][:70]}", 0.0))
        if moved:
            self.scene._nudges.append(
                (self.beat.anchor[:44], stage._describe(group), round(moved, 3)))

    def retire(self, *tags: str, run_time: float = 0.35):
        """
        Remove tagged content. Silently ignores tags already gone.

        A group can be *owned* without being the thing the scene actually holds:
        a beat that builds a graph node by node adds each node individually and
        then owns the collecting VGroup. Fading that VGroup removes nothing,
        because the scene never had it — the children linger and collide with
        whatever comes next, two minutes later. So fade whichever of
        group-or-children the scene is really holding.
        """
        on_stage = {id(m) for m in self.scene.mobjects}
        targets: list[Mobject] = []
        for tag in tags:
            group = self.scene._owned.pop(tag, None)
            if group is None:
                continue
            if id(group) in on_stage:
                targets.append(group)
                continue
            kids = [m for m in group.submobjects if id(m) in on_stage]
            if not kids:
                kids = [m for m in group.get_family() if id(m) in on_stage]
            targets.extend(kids)
        if not targets:
            return
        rt = self.budget(run_time)[0]
        self.scene.play(*[FadeOut(m) for m in targets], run_time=rt)

    def clear_stage(self, *keep_tags: str, run_time: float = 0.6):
        """
        Empty the stage except for the title and the tags named.

        Retiring content tag by tag is reliable only if every tag is remembered,
        and at an act boundary — where the argument restarts and the picture
        should restart with it — forgetting one leaves a shape from two minutes
        ago sitting under the new composition. That is not a defect the geometry
        checks can catch, because a stale *shape* overlaps nothing and says
        nothing; it just quietly makes the frame wrong.

        So the boundary is stated positively: keep these, drop everything else.
        """
        keep: set[int] = {id(self.scene._title)} if self.scene._title is not None else set()
        for tag in keep_tags:
            group = self.scene._owned.get(tag)
            if group is not None:
                keep |= {id(m) for m in group.get_family()} | {id(group)}
        going = [m for m in self.scene.mobjects if id(m) not in keep]
        for tag in list(self.scene._owned):
            if tag not in keep_tags:
                self.scene._owned.pop(tag)
        if self.scene._caption is not None and id(self.scene._caption) not in keep:
            self.scene._caption = None
        if not going:
            return
        rt = self.budget(run_time)[0]
        self.scene.play(*[FadeOut(m) for m in going], run_time=rt)

    def waive(self, check: str, reason: str):
        """
        Declare that a check does not apply to this beat, and say why.

        The alternative — loosening a threshold until the check stops finding the
        deliberate case — also stops it finding the accidental ones, everywhere,
        for the rest of the video. A waiver is local, dated to a beat, and has to
        carry a reason a reader can disagree with.
        """
        self.scene.qa_waive(check, self.beat.start - 0.4,
                            self.beat.start + self.beat.window + 0.4, reason)

    def lopsided(self, reason: str):
        """Declare that this beat's composition is meant to be off-centre."""
        self.waive("stage_imbalance", reason)

    def recede(self, *tags: str, opacity: float = 0.16, run_time: float = 0.4,
               keep_edges: bool = False):
        """
        Push content into the background — connectors included.

        Dimming a diagram by tag misses the lines between its nodes, because the
        lines are owned under different tags. The result is a picture that has
        supposedly receded but still has every connector at full strength drawn
        across it, which is what makes a dimmed diagram read as clutter instead
        of as background. Six of the reviewer's notes were that one thing.

        So this dims what you name *and* every connector on stage whose ends land
        on it. Pass keep_edges=True for the rare case where the lines really are
        the subject and the nodes are not.
        """
        targets = [self.scene._owned[t] for t in tags if t in self.scene._owned]
        if not targets:
            return
        boxes = []
        for g in targets:
            boxes.append((g.get_left()[0], g.get_right()[0],
                          g.get_bottom()[1], g.get_top()[1]))

        def touches(point) -> bool:
            return any(x0 - 0.35 <= point[0] <= x1 + 0.35
                       and y0 - 0.35 <= point[1] <= y1 + 0.35
                       for x0, x1, y0, y1 in boxes)

        extra = []
        if not keep_edges:
            for top in self.scene.mobjects:
                for m in top.get_family():
                    # The whole connector group, not just its stroke: a
                    # glow_arrow is an aura plus a core, and only the core
                    # carries the role tag. Dimming the core alone leaves the
                    # aura burning at full strength, which is still a bright
                    # line across a dimmed picture.
                    if getattr(m, "qa_layer", None) != "edge":
                        continue
                    core = next((k for k in m.get_family()
                                 if getattr(k, "qa_role", None) == "edge"), None)
                    if core is None:
                        continue
                    try:
                        ends = (core.get_start(), core.get_end())
                    except Exception:
                        continue
                    if any(touches(e) for e in ends):
                        extra.append(m)
        # A stroke has to go lower than a shape to recede by the same amount. A
        # filled node at 35% washes out; a one-pixel saturated line at 35% still
        # reads as a bright line drawn across the picture, which is why dimming
        # both to the same number left the diagram looking cluttered even after
        # the connectors were included.
        edge_opacity = max(opacity * 0.5, 0.06)
        rt = self.budget(run_time)[0]
        self.scene.play(*[g.animate.set_opacity(opacity) for g in targets
                          if getattr(g, "qa_layer", None) != "edge"],
                        *[g.animate.set_opacity(edge_opacity) for g in targets
                          if getattr(g, "qa_layer", None) == "edge"],
                        *[e.animate.set_opacity(edge_opacity) for e in extra],
                        run_time=rt)


    def caption(self, text: str, color: str = style.WHITE, force: bool = False):
        """
        Put a line in the caption lane.

        Captions never collide with the diagram because the lane is reserved and
        the diagram is fitted outside it. They also cannot be cued to a line that
        is too short to read them: a caption needs MIN_CAPTION_HOLD seconds, and
        asking for one inside a shorter window is a storyboard error, raised at
        build time rather than discovered in review.

        Fast narration should change the *diagram*, not flash a caption.
        """
        if self.window < MIN_CAPTION_HOLD and not force:
            raise ValueError(
                f"caption {text!r} is cued to a {self.window:.1f}s window but needs "
                f"{MIN_CAPTION_HOLD:.1f}s to stay readable at {EXPORT_SPEED}x. "
                "Change the diagram on this line instead, or move the caption to a "
                "longer line. Pass force=True only for a deliberate flash."
            )
        cap = style.caption_text(text, color=color)
        stage.fit(cap, stage.CAPTION)
        self.scene._set_caption(cap, self.budget(0.4)[0], self.window)
        return cap

    def play(self, *anims, run_time: float = 0.6):
        self.scene.play(*anims, run_time=self.budget(run_time)[0])

    def hold(self, seconds: float = 0.3):
        self.scene.wait(min(seconds, max(self.window, 0.05)))


class BeatScene(QASceneMixin, Scene):
    """
    A section of the video.

    Subclasses declare `section_id` and `storyboard()`. Everything else — timing,
    caption lane management, ownership, QA capture — happens here.
    """

    section_id: str = ""
    timing_dir: Path = Path("out/timing")
    title: str = ""

    # Review builds carry a slate in the top-left: section, beat number and the
    # time within the scene. It gives the reviewer something exact to point at —
    # "S03 b17" beats "the bit with the bars" — and it is off for delivery.
    review_slate: bool = bool(int(os.environ.get("VC_REVIEW_SLATE", "0")))

    def storyboard(self) -> list[Beat]:
        raise NotImplementedError

    # -- internals --------------------------------------------------------
    def setup(self):
        super().setup()
        self.camera.background_color = style.BG
        self._owned: dict[str, VGroup] = {}
        self._nudges: list[tuple[str, str, float]] = []
        self._idle: list[tuple[int, str, float]] = []
        self._slate: Mobject | None = None
        self._title: Mobject | None = None
        self._caption: Mobject | None = None
        self._caption_since: float = 0.0

    def add(self, *mobjects):
        """
        Add to the scene, keeping connectors on the back layer.

        Doing this in `ctx.show` was not enough: scenes create edges with
        `play(Create(edge))`, which calls `add` directly and put the connector on
        top of the nodes it joins. It then appeared to flip behind them the
        moment anything else was added — which is exactly the blinking-to-back
        artefact. Enforcing it here covers every route into the scene.
        """
        super().add(*mobjects)
        for mob in mobjects:
            if getattr(mob, "qa_layer", None) == "edge" or any(
                    getattr(s, "qa_role", None) == "edge" for s in mob.get_family()):
                super().bring_to_back(mob)
        return self

    def play(self, *args, **kwargs):
        """
        Play, having first placed any connector on the back layer.

        Introducer animations (`Create`, `FadeIn`, `Write`) add their mobject
        through a path that skips `Scene.add`, so an edge created with
        `play(Create(edge))` slipped past the layering rule and was drawn over
        the very nodes it attaches to. Seating it before the animation begins
        also avoids the half-second where it is briefly on top.
        """
        for arg in args:
            mob = getattr(arg, "mobject", None)
            if mob is None:
                continue
            is_edge = getattr(mob, "qa_layer", None) == "edge" or any(
                getattr(s, "qa_role", None) == "edge" for s in mob.get_family())
            if is_edge and mob not in self.mobjects:
                self.add(mob)

        before = list(self.mobjects)
        result = super().play(*args, **kwargs)

        # `something.animate` on an ad-hoc VGroup of mobjects already on stage
        # adds that wrapper to the scene, and Manim's own `add` then absorbs the
        # children into it — so the whole group jumps to the front of the draw
        # order. That is how connectors ended up over the nodes they attach to
        # and appeared to flip layer.
        #
        # The wrapper has to go, but it cannot simply be removed: because the
        # children were absorbed, dropping the wrapper drops them too, and they
        # vanish until some later beat happens to re-add them. That is exactly
        # the blink the reviewer saw — thirty-four chips disappearing for a
        # second and a half, and the whole left column of the two-worlds picture
        # blipping out before the bottleneck beat. So put the children back,
        # where they were, rather than at the end.
        for mob in list(self.mobjects):
            if mob in before or not isinstance(mob, VGroup) or not mob.submobjects:
                continue
            # Any child already on stage means this is a wrapper around existing
            # content, not new content. Requiring *all* children to be present
            # missed the common case — a group built from one live mobject and
            # one collecting VGroup that was never added.
            # Family, not direct children. A beat that wraps two *owned groups*
            # — `VGroup(self._owned["more"], self._owned["stream"])` — puts the
            # live chips two levels down, so looking only at direct children
            # finds nothing to restore and the chips stay swallowed.
            before_ids = {id(m) for m in before}
            restore = [c for c in mob.get_family() if id(c) in before_ids]
            if not restore:
                continue
            index = self.mobjects.index(mob)
            self.remove(mob)
            on_stage = {id(m) for m in self.mobjects}
            kept = [c for c in restore if id(c) not in on_stage]
            if kept:
                # Rebuild the list by hand: Scene.add appends, which would put
                # them in front of everything and re-create the layering bug
                # this block exists to undo.
                index = min(index, len(self.mobjects))
                self.mobjects[index:index] = kept

        # Re-assert the invariant rather than trying to predict every route a
        # mobject can take into the scene. Connectors belong behind the things
        # they join, always; cheapest to simply restate it once per animation.
        _seat_edges(self)
        return result

    def _own(self, tag: str, group: VGroup):
        if tag in self._owned:
            raise ValueError(f"tag {tag!r} is already on stage; retire it first")
        self._owned[tag] = group

    def _set_caption(self, cap: Mobject, run_time: float, window: float):
        """
        Swap the caption lane's occupant.

        The outgoing caption is held to its minimum only as far as the incoming
        beat's window allows — readability must never be bought with drift, since
        drift is cumulative and unrecoverable.
        """
        now = self.renderer.time
        if self._caption is not None:
            held = now - self._caption_since
            short_by = MIN_CAPTION_HOLD - held
            if short_by > 0:
                self.wait(min(short_by, max(window - run_time - 0.1, 0.0)))
            self.play(FadeOut(self._caption), FadeIn(cap), run_time=run_time)
        else:
            self.play(FadeIn(cap), run_time=run_time)
        self._caption = cap
        self._caption_since = self.renderer.time

    def construct(self):
        lines = timing.load(self.section_id, self.timing_dir)
        beats = self.storyboard()

        # Resolve every anchor before animating anything, so a broken anchor
        # fails immediately instead of halfway through a render.
        for beat in beats:
            line = timing.resolve_anchor(beat.anchor, lines)
            beat.start = max(line.start - beat.lead, 0.0)
        beats.sort(key=lambda b: b.start)
        # Run to the end of the audio file, not the last word: the tail of a take
        # is silence, and stopping early leaves a frozen frame under it.
        audio_end = timing.audio_duration(self.section_id, self.timing_dir) \
            or max(l.end for l in lines)
        for beat, nxt in zip(beats, beats[1:] + [None]):
            beat.window = (nxt.start if nxt else audio_end) - beat.start

        if self.title:
            t = style.title_text(self.title)
            stage.fit(t, stage.TITLE)
            self._title = t
            self.play(FadeIn(t, shift=DOWN * 0.12), run_time=0.45)

        for n, beat in enumerate(beats, 1):
            lag = beat.start - self.renderer.time
            if lag > 0.02:
                self.wait(lag)
            # A beat that finishes well inside its window leaves the picture
            # frozen until the next cue. That is dead air, and it was invisible
            # until now because it belongs to the *previous* beat's window while
            # being spent in this beat's wait. Attribute it where it is owned.
            if lag > IDLE_LIMIT and n > 1:
                self._idle.append((n - 1, beats[n - 2].anchor[:44], round(lag, 2)))
            if self.review_slate:
                self._set_slate(n, beat)
            beat.build(BeatContext(self, beat))

        tail = audio_end - self.renderer.time
        if tail > 0.05:
            self.wait(tail)

        self._dump_beats(beats, lines)
        if self._idle:
            print(f"  idle gaps ({len(self._idle)}) — beats that end early and "
                  f"leave the frame frozen:")
            for n, anchor, secs in self._idle:
                print(f"    {secs:5.1f}s after b{n:02d}  {anchor!r}")
        if self._nudges:
            # Surfaced, not silent. A nudge is the pipeline making a placement
            # decision the storyboard did not make, and a label that needs a big
            # one is telling you the composition is crowded, not that the
            # placement helper is clever.
            print(f"  layout nudges ({len(self._nudges)}):")
            for anchor, what, dist in self._nudges:
                print(f"    {dist:+.2f}  {what:44} @ {anchor!r}")

    def _set_slate(self, n: int, beat: Beat) -> None:
        """Update the review slate. Not part of the delivered frame."""
        code = f"{self.slate_prefix} b{n:02d}  {beat.start:6.1f}s"
        slate = Text(code, font=style.MONO, font_size=17, color=style.AMBER)
        slate.to_corner(UL, buff=0.22)
        slate.set_z_index(style.Z_SLATE, family=True)
        if getattr(self, "_slate", None) is not None:
            self.remove(self._slate)
        self._slate = slate
        if isinstance(self, ThreeDScene):
            self.add_fixed_in_frame_mobjects(slate)
        else:
            self.add(slate)
        # The slate must never be judged as part of the composition.
        for sub in slate.get_family():
            sub.qa_ignore = True

    @property
    def slate_prefix(self) -> str:
        return (self.section_id.split("_")[0] or "S").upper()

    def _dump_beats(self, beats: list[Beat], lines) -> None:
        """
        Record what each beat was cued to, for the review page.

        The reviewer needs the narration line beside the visual it drives. Video
        1's review tooling guessed that pairing from an elapsed-time ratio and got
        it wrong on any section with an uneven speaking rate.
        """
        import json
        out = Path(self.timing_dir).parent / "beats"
        out.mkdir(parents=True, exist_ok=True)
        payload = []
        for beat in beats:
            line = min(lines, key=lambda l: abs(l.start - beat.start))
            payload.append({
                "anchor": beat.anchor, "note": beat.note,
                "start": round(beat.start, 3), "window": round(beat.window, 3),
                "line": line.text, "line_index": line.index,
                "confidence": line.confidence,
            })
        (out / f"{type(self).__name__}.beats.json").write_text(
            json.dumps({"scene": type(self).__name__, "section": self.section_id,
                        "beats": payload}, indent=2) + "\n")


def _is_edge(mob: Mobject) -> bool:
    return getattr(mob, "qa_layer", None) == "edge" or getattr(mob, "qa_role", None) == "edge"


def _seat_edges(scene: Scene) -> None:
    """
    Put every connector behind the things it joins — at any nesting depth.

    Top-level ordering is not enough. A scene that collects nodes and edges into
    one group (`chain.add(node, edge)`) draws each edge *after* its own node, so
    the connector sits on top of the shape it attaches to no matter where the
    group sits in the scene. Reordering within each group is what actually fixes
    it, and re-asserting the whole invariant after every animation is cheaper
    than predicting every route a mobject can take into the scene.
    """
    def sort_group(group: Mobject) -> None:
        kids = list(group.submobjects)
        if len(kids) > 1:
            edges = [k for k in kids if _is_edge(k) or any(_is_edge(s) for s in k.get_family())]
            if edges and len(edges) < len(kids):
                rest = [k for k in kids if k not in edges]
                group.submobjects = edges + rest
        for kid in group.submobjects:
            if kid.submobjects:
                sort_group(kid)

    top_edges = []
    for mob in scene.mobjects:
        if mob.submobjects:
            sort_group(mob)
        if _is_edge(mob) or any(_is_edge(s) for s in mob.get_family()):
            if all(_is_edge(s) or not s.submobjects for s in mob.submobjects) and _is_edge(mob):
                top_edges.append(mob)
    if top_edges:
        scene.bring_to_back(*top_edges)


# ------------------------------------------------------------- transitions --
# Section-to-section transitions are declared, not hand-rolled, so the whole
# video has a consistent grammar and any of them can be changed in one place.

def cut(scene: Scene):
    """Hard cut. Everything leaves at once."""
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=0.35)


def settle(scene: Scene, keep: list[Mobject] | None = None):
    """
    Everything leaves except what carries the argument forward.

    Use when the next section builds on this one's picture — the graph stays, the
    annotation around it goes. Reading continuity is the point.
    """
    keep = keep or []
    going = [m for m in scene.mobjects if m not in keep]
    if going:
        scene.play(*[FadeOut(m) for m in going], run_time=0.4)


def pull_back(scene: ThreeDScene, phi: float = 62, theta: float = -40, run_time: float = 1.4):
    """Reveal that the thing just examined is part of something larger."""
    scene.move_camera(phi=phi * DEGREES, theta=theta * DEGREES, run_time=run_time)
