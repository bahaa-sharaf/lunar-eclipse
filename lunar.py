# Made by Bahaa Sharaf (https://github.com/bahaa-sharaf)

from  manim import *

class planetsv3(ThreeDScene):
    def construct(self):
        # Cam zoom (zoom=.6, phi=0*DEGREES, theta=-90*DEGREES)
        self.set_camera_orientation(zoom=.6, phi=0*DEGREES, theta=-90*DEGREES)

        # Axes and labels
        ext = 15
        axes = ThreeDAxes(x_length=ext, y_length=ext, x_range=(-ext,ext,1), y_range=(-ext,ext,1), tips=False, axis_config={"color": GRAY, "stroke_opacity": 0.1})
        # x_label = axes.get_x_axis_label("x").shift(RIGHT*1.5)
        # y_label = axes.get_y_axis_label("y", rotation=PI*2).shift(UP*1)
        # z_label = axes.get_z_axis_label("z")
        xy_plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[-ext,ext],  # Range for u (x-axis)
            v_range=[-ext,ext],  # Range for v (y-axis)
            resolution=ext,
            checkerboard_colors=[BLACK, WHITE],
            fill_opacity=.05,
            stroke_width=0)

        # Planets
        sun = Sphere(resolution=(12,24), radius=0.8)
        sun.set_fill(ORANGE)
        earth = Sphere(resolution=(6,12), radius=0.25).shift(RIGHT*5.5)
        earth.set_fill(BLUE)
        moon = Sphere(resolution=(6,12), radius=0.1).shift(RIGHT*6.8)
        moon.set_fill(GRAY_B)
        earth_path = Circle(radius=5.5, color=WHITE, stroke_width=1, stroke_opacity=0.5)
        moon_path = Circle(radius=1.3, color=WHITE, stroke_width=1, fill_opacity=0.20).shift(RIGHT*5.5)

        # Add an updater function to make the moon_path follow the earth
        def follow_rule(mob):
        # Set the moon_path's position to the earth's position
            mob.move_to(earth.get_center())
        # Add the updater to the moon_path
        moon_path.add_updater(follow_rule)

        # Rotate moon_path
        moon_path.rotate(10 * DEGREES, axis=DOWN, about_point=earth.get_center())

        # Earth's shadow and penumbra lines
        sun_top = np.array([0,0,sun.radius])
        sun_bottom = np.array([0,0,-sun.radius])
        earth_top = np.array([earth_path.radius,0,earth.radius])
        earth_bottom = np.array([earth_path.radius,0,-earth.radius])

        # Function to calculate new_end_point
        def CalcEndPoint(start_point, end_point, extension_length):
            # Calculate the direction vector of the line
            direction = (end_point - start_point)
            # Calculate the new endpoint by extending in the direction of the line
            new_end_point = end_point + direction * extension_length
            return new_end_point

        extension_length = scale = 0.45
        line11 = Line(sun_top,CalcEndPoint(sun_top, earth_bottom, extension_length)).set_color(ORANGE)
        line12 = Line(sun_bottom,CalcEndPoint(sun_bottom, earth_top, extension_length)).set_color(ORANGE)
        line13 = Line(sun_top,CalcEndPoint(sun_top, earth_top, extension_length)).set_color(TEAL)
        line14 = Line(sun_bottom,CalcEndPoint(sun_bottom, earth_bottom, extension_length)).set_color(TEAL)

        lines1 = VGroup(line11, line12, line13, line14)
        lines1.set_stroke(width=1.5)
        
        # Highlighting Umbra and Penumbra
        # Calculate extended points for lines (Points A, B, C)
        def ExtendPoint(start, end):
            direction = end - start
            return end + direction * scale

        point_a = ExtendPoint(sun_bottom, earth_top)
        point_b = ExtendPoint(sun_top, earth_top)
        point_c = ExtendPoint(sun_top, earth_bottom)

        # Shadow region (Umbra)
        umbra1 = Polygon(earth_top, earth_bottom, point_b,
                         color=TEAL, fill_opacity=0.30).set_stroke(opacity=0)

        # Penumbra region
        penumbra11 = Polygon(earth_top, point_a, point_b)
        penumbra12 = Polygon(earth_bottom, point_b, point_c)
        penumbra1 = VGroup(penumbra11, penumbra12)
        penumbra1.set_color(ORANGE).set_opacity(0.225).set_stroke(opacity=0)

        # Umbra2, Penumbra2, Lines2
        umbra2 = umbra1.rotate(90*DEGREES, OUT, about_point=ORIGIN)
        penumbra2 = penumbra1.rotate(90*DEGREES, OUT, about_point=ORIGIN)
        lines2 = lines1.rotate(90*DEGREES, OUT, about_point=ORIGIN)
        # UPL2 = VGroup(umbra1, penumbra1, lines1).rotate(90*DEGREES, OUT, about_point=ORIGIN)



        '''ANIMATIONS'''
        # Add the axes and labels to the scene
        self.add(axes, xy_plane)
        self.add(sun, earth, earth_path, moon_path)
        self.wait(3)

        # Moon and Earth animations
        for _ in range(2):
            self.play(MoveAlongPath(earth, earth_path),
                      MoveAlongPath(moon, moon_path),
                      run_time=10, rate_func=linear)
        self.wait(3)

        # Cam moves to eye level
        self.move_camera(zoom=.95, phi=90*DEGREES, theta=-90*DEGREES, run_time=6)
        self.wait(3)

        # Moon and Earth animations
        for _ in range(1):
            self.play(MoveAlongPath(earth, earth_path),
                      MoveAlongPath(moon, moon_path),
                      run_time=10, rate_func=linear)
        self.wait(3)

        # Fade Out moons orbit
        self.play(moon_path.animate.set_opacity(0.15), run_time=0.75)
        self.wait(0.5)

        # Earth shadow and penumbra drawing
        self.play(Create(line13), Create(line14))
        self.wait(0.5)
        self.play(Create(line11), Create(line12))
        self.wait(2)

        # Earth shadow and penumbra highlighting
        self.play(FadeIn(umbra1), run_time=2)
        self.play(FadeIn(penumbra1), run_time=2)
        self.wait(4)

        # Reset scene
        self.play(moon_path.animate.set_stroke(opacity=1).set_fill(opacity=0.2),
                  FadeOut(umbra1, penumbra1), run_time=0.75)



        # Moon and earth animation for quarter 1
        self.play(MoveAlongPath(earth, earth_path),
                  MoveAlongPath(moon, moon_path),
                  rate_func=lambda t: t * 0.25,  # Move only 25% (quarter) of the path
                  run_time=2.5)
        self.wait(3)

        # Cam moves to quarter 2
        self.move_camera(zoom=.95, phi=90*DEGREES, theta=0*DEGREES, run_time=3)
        self.wait(3)

        # Fade Out moons orbit
        self.play(moon_path.animate.set_opacity(0.15), run_time=0.75)
        self.wait(0.5)

        # Earth shadow and penumbra drawing
        self.play(Create(lines2), run_time=4)
        self.wait(3)

        # Earth shadow and penumbra highlighting
        self.play(FadeIn(umbra2), run_time=2)
        self.play(FadeIn(penumbra2), run_time=2)
        self.wait(4)

        # Reset scene
        self.play(moon_path.animate.set_stroke(opacity=1).set_fill(opacity=0.2),
                  FadeOut(umbra1, penumbra1), run_time=0.75)
