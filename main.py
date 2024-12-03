from manim import *


class MyScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=-0 * DEGREES)

        axes = ThreeDAxes()

        circle = Circle()  # create a circle
        circle.set_fill(ORANGE, opacity=1.0)  # set the color and transparency

        # Create the vertical bar of the upright T
        vertical_bar = Rectangle(height=1, width=0.5, color=ORANGE)

        # Create the horizontal bar of the upright T
        horizontal_bar = Rectangle(height=0.5, width=2, color=ORANGE)
        horizontal_bar.next_to(vertical_bar, UP, buff=0)  # Position above the vertical bar

        # Group to form the upright T shape
        upright_t = VGroup(vertical_bar, horizontal_bar)

        # Create the vertical bar of the inverted T
        inverted_vertical_bar = Rectangle(height=1, width=0.5, color=ORANGE)

        # Create the horizontal bar of the inverted T
        inverted_horizontal_bar = Rectangle(height=0.5, width=2, color=ORANGE)
        inverted_horizontal_bar.next_to(inverted_vertical_bar, DOWN, buff=0)  # Position below the vertical bar

        # Group to form the inverted T shape
        inverted_t = VGroup(inverted_vertical_bar, inverted_horizontal_bar)

        # Position the inverted T beneath the upright T
        inverted_t.next_to(upright_t, DOWN, buff=0.5)

        # Group both T shapes and center them
        both_t_shapes = VGroup(upright_t, inverted_t)
        both_t_shapes.move_to(ORIGIN)  # Center the group on the screen
        both_t_shapes.set_fill(ORANGE, opacity=1.0)  # set the color and transparency

        # Transform the circle into the T shapes
        self.play(FadeIn(circle))  # Show the circle
        self.wait(1)
        self.play(Transform(circle, both_t_shapes))  # Transform the circle into the T shapes
        self.wait(2)

        self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='phi')
        self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='theta')
        self.wait(2)
        self.stop_ambient_camera_rotation(about='phi')