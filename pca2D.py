from manim import *
import numpy as np


# Define the wave packet function
def wave_packet(x, t):
    amplitude = 0.5 * np.exp(-1.0 * (x - t) ** 2)  # Smaller amplitude and narrower Gaussian envelope
    frequency = 5 * (x - t)  # Oscillation
    return amplitude * np.sin(frequency)


def thz_dummy_pulse(x):
    return np.sin(x) ** 63 * np.sin(x + 1.5) * 8


class MyScene(Scene):
    def construct(self):
        # Create a rectangle and a semicircle
        semicircle = Arc(radius=1, angle=PI, arc_center=ORIGIN)
        semicircle.rotate(-90 * DEGREES, about_point=ORIGIN)
        line = Line([0, -1, 0], [0, 1, 0])
        semicircle.next_to(line, RIGHT, buff=0.0)
        semicircle.set_fill(color=GRAY, opacity=0.5)

        Silicon = VGroup(line, semicircle)
        Silicon.set_fill(GRAY)

        Title = Text("Photoconductive Antenna (PCA)")
        Title.move_to([0, 2.5, 0])

        Substrate = Rectangle(width=0.05, height=2, color=BLUE, fill_color=BLUE, fill_opacity=1)
        Substrate.next_to(Silicon, LEFT, buff=0.0)

        anode = Rectangle(width=0.05, height=0.8, color=ORANGE, fill_opacity=1)
        cathode = Rectangle(width=0.05, height=0.8, color=ORANGE, fill_opacity=1)
        anode.move_to([0, 0.5, 0])
        cathode.move_to([0, -0.5, 0])

        Electrodes = VGroup(anode, cathode)
        Electrodes.set_fill(ORANGE)
        Electrodes.next_to(Substrate, LEFT, buff=0.0)

        wire1 = Line([-0.075, 0.9, 0], [-0.075, 1.5, 0])
        wire2 = Line([-0.075, 1.5, 0], [-1, 1.5, 0])
        wire3 = Line([-1, 1.5, 0], [-1, -0.6, 0])
        wire4 = Line([-1.3, -0.6, 0], [-0.7, -0.6, 0])
        wire5 = Line([-1.2, -0.8, 0], [-0.8, -0.8, 0])
        wire6 = Line([-1, -0.8, 0], [-1, -1.5, 0])
        wire7 = Line([-1, -1.5, 0], [-0.075, -1.5, 0])
        wire8 = Line([-0.075, -1.5, 0], [-0.075, -0.9, 0])
        Circuit = VGroup(wire1, wire2, wire3, wire4, wire5, wire6, wire7, wire8)

        # Add the rectangle, semicircle, and photon to the scene
        self.play(Create(Circuit), Create(Silicon), Create(Title), Create(Electrodes), Create(Substrate))

        # Create a time tracker for animation
        self.time_tracker = ValueTracker(0)

        # Create a Wave packet as a ParametricFunction
        Wave = always_redraw(lambda: ParametricFunction(
            lambda t: np.array([
                t, wave_packet(t + 7, self.time_tracker.get_value()), 0
            ]),
            t_range=np.array([-5, -0.01, 0.01]),
            color=RED
        ))

        # Create a blue Cone emanating to the right
        Cone = Polygon(
            RIGHT * 0.1 + UP * 1,  # Top vertex
            RIGHT * 5,  # Right vertex
            RIGHT * 0.1 + DOWN * 1,  # Bottom vertex
            color=BLUE,
            fill_opacity=0.5
        )
        Cone.set_stroke(width=0)  # Hide outline for smooth effect
        Cone.rotate(180 * DEGREES)

        # Add the rectangle and Wave packet to the scene
        self.play(Create(Wave))

        # Animate the Wave packet moving through the rectangle
        self.play(self.time_tracker.animate.set_value(9), run_time=1, rate_func=linear)

        # Add and grow the Cone
        self.play(GrowFromPoint(Cone, point=Cone.get_left(), run_time=1), rate_func=linear)
        self.wait(1)

        self.play(FadeOut(Cone), FadeOut(Wave), FadeOut(Title))

        PCA = VGroup(Electrodes, Silicon, Circuit, Substrate)

        # Increase the size of everything to zoom in without increasing the stroke width
        self.play(PCA.animate.scale(30).move_to([-5, -0.1, 0]), run_time=2)

        # Keep everything on screen
        self.wait(1)

        # draw electric field
        arrow1 = Arrow(end=[-2.25, -3, 0], start=[-2.25, 3, 0], stroke_width=1.0, fill_opacity=0.5)
        arrow2 = Arrow(end=[-2.80, -3, 0], start=[-2.80, 3, 0], stroke_width=1.0, fill_opacity=0.5)
        arrow3 = Arrow(end=[-3.35, -3, 0], start=[-3.35, 3, 0], stroke_width=1.0, fill_opacity=0.5)
        field = Tex(r"$\vec{E}$", font_size=100)
        field.move_to([-4.5, 2.5, 0])
        self.play(FadeIn(field), Create(arrow1), Create(arrow2), Create(arrow3))
        self.wait(1)

        laser = Line([-10, 0, 0], [-2, 0, 0], color=RED, stroke_width=100)
        self.play(Create(laser))

        electrons = []
        holes = []
        texts = []
        for i in range(3):
            electron = Circle(radius=0.3, color=ORANGE, fill_opacity=1)
            electron.move_to([-1.25, 0.5 + i, 0])
            electrons.append(electron)
            hole = Circle(radius=0.3, color=BLACK, fill_opacity=1)
            hole.move_to([-1.25, - 0.5 - i, 0])
            holes.append(hole)
            text = Tex(r"e$^{-}$")
            text.move_to([-1.25, 0.5 + i, 0])
            texts.append(text)
            self.play(FadeIn(hole), FadeIn(electron), FadeIn(text), run_time=0.1)

        thz_pulse = ParametricFunction(
            lambda t: np.array([
                t, thz_dummy_pulse(t), 0
            ]),
            t_range=np.array([4, 5.5, 0.01]),
            color=BLUE
        )

        thz_pulse.move_to([1, 0, 0])
        self.add(thz_pulse)

        self.play(FadeOut(laser), *[electron.animate.move_to([-1.25, 2.5, 0]) for electron in electrons],
                  *[text.animate.move_to([-1.25, 2.5, 0]) for text in texts],
                  *[hole.animate.move_to([-1.25, -2.5, 0]) for hole in holes],
                  thz_pulse.animate.move_to([10, 0, 0]), rate_func=linear)

        self.play(
            *[FadeOut(hole) for hole in holes],
            *[FadeOut(text) for text in texts],
            *[FadeOut(electron) for electron in electrons],
            run_time=0.1)
        self.wait(1)
