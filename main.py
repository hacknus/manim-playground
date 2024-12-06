from manim import *


class MyScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=45 * DEGREES, theta=30 * DEGREES)

        # Create 3D axes
        axes = ThreeDAxes()

        # Prism dimensions (matching the T-shape)
        prism_length = 4  # Length of the top bar of T
        prism_width = 4  # Width of the T
        prism_thickness = 0.1  # Thickness of the prism

        # Create the prism
        Substrate = Prism(dimensions=[prism_length, prism_width, prism_thickness])
        Substrate.set_fill(BLUE, opacity=1.0)
        Substrate.set_stroke(BLUE_E, width=2)

        # Create the T-shape using VMobject (half-size)
        t_shape = VMobject()
        t_shape.set_fill(ORANGE, opacity=1.0)
        t_shape.set_stroke(RED, width=4)

        # Define the T-shape's vertices
        t_shape.set_points_as_corners([
            [-1, 0.5, 0],  # Top-left corner of T
            [1, 0.5, 0],  # Top-right corner of T
            [1, 0, 0],  # Bottom-right corner of top bar
            [0.25, 0, 0],  # Right side of vertical bar
            [0.25, -1, 0],  # Bottom-right of vertical bar
            [-0.25, -1, 0],  # Bottom-left of vertical bar
            [-0.25, 0, 0],  # Left side of vertical bar
            [-1, 0, 0],  # Bottom-left corner of top bar
            [-1, 0.5, 0],  # Back to start to close the shape
        ])

        # Create an inverted T-shape (mirrored vertically)
        inverted_t_shape = VMobject()
        inverted_t_shape.set_fill(ORANGE, opacity=1.0)
        inverted_t_shape.set_stroke(RED, width=4)

        # Define the inverted T-shape's vertices
        inverted_t_shape.set_points_as_corners([
            [-1, -0.5, 0],  # Bottom-left corner of inverted T
            [1, -0.5, 0],  # Bottom-right corner of inverted T
            [1, 0, 0],  # Top-right corner of bottom bar
            [0.25, 0, 0],  # Right side of vertical bar
            [0.25, 1, 0],  # Top-right of vertical bar
            [-0.25, 1, 0],  # Top-left of vertical bar
            [-0.25, 0, 0],  # Left side of vertical bar
            [-1, 0, 0],  # Top-left corner of bottom bar
            [-1, -0.5, 0],  # Back to start to close the shape
        ])
        t_shape.shift(UP * 1.5)
        inverted_t_shape.shift(DOWN * 1.5)

        # Position the shapes for visibility
        both_t_shapes = VGroup(t_shape, inverted_t_shape)
        both_t_shapes.move_to([0, 0, -0.1])  # Position on the opposite side of the prism

        # Create a Silicon (using a sphere scaled by 0.5 in the Z-axis)
        Silicon = Sphere(radius=2.0, u_range=[0.0, PI], v_range=[0.0, PI])
        Silicon.set_fill(GRAY, opacity=1.0)
        Silicon.move_to([0, 0, 1])  # Position on the opposite side of the prism
        Silicon.rotate(angle=90 * DEGREES, axis=RIGHT)  # Rotate around the Y-axis

        # Add all objects to the scene
        self.add(Substrate, both_t_shapes, Silicon)
        # Apply depth test to avoid visibility issues through objects
        Substrate.set_depth_test(True)
        both_t_shapes.set_depth_test(True)
        Silicon.set_depth_test(True)

        # Camera movements
        self.begin_ambient_camera_rotation(rate=0.1)  # Slow rotation
        self.wait(10)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=75 * DEGREES, theta=45 * DEGREES, zoom=1.2)
        self.wait(5)
