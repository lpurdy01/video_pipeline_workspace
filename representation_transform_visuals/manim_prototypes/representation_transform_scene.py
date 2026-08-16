from manim import *


class RepresentationTransformPipeline(Scene):
    def construct(self):
        title = Text("Representation Transform", font_size=44)
        title.to_edge(UP)

        input_box = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.12)
        input_label = Text("English\nrequirement", font_size=26).move_to(input_box)
        input_group = VGroup(input_box, input_label).shift(LEFT * 4)

        vector_space = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3.0,
            y_length=2.2,
            tips=False,
        )
        dots = VGroup(
            Dot(vector_space.c2p(-1.1, 0.4), color=BLUE),
            Dot(vector_space.c2p(-0.2, 1.0), color=TEAL),
            Dot(vector_space.c2p(0.8, 0.2), color=YELLOW),
            Dot(vector_space.c2p(1.1, -0.8), color=RED),
        )
        space_label = Text("learned\nvector space", font_size=24).next_to(vector_space, DOWN)
        space_group = VGroup(vector_space, dots, space_label)

        output_box = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.12)
        output_label = Text("code + tests\n+ evidence", font_size=26).move_to(output_box)
        output_group = VGroup(output_box, output_label).shift(RIGHT * 4)

        left_arrow = Arrow(input_group.get_right(), space_group.get_left(), buff=0.25)
        right_arrow = Arrow(space_group.get_right(), output_group.get_left(), buff=0.25)

        warning = Text("powerful, useful, and lossy", font_size=28, color=YELLOW)
        warning.to_edge(DOWN)

        self.play(Write(title))
        self.play(FadeIn(input_group), GrowArrow(left_arrow))
        self.play(Create(vector_space), FadeIn(dots), FadeIn(space_label))
        self.play(GrowArrow(right_arrow), FadeIn(output_group))
        self.play(Write(warning))
        self.wait(2)

