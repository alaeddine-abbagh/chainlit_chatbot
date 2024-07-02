from manim import *
import numpy as np

class TriangleAnglesSum(Scene):
    def construct(self):
        # Create a triangle
        triangle = Polygon([-3, -1.5, 0], [3, -1.5, 0], [0, 2, 0], color=WHITE)
        
        # Create labels for the angles
        labels = VGroup(
            MathTex(r"\alpha").move_to([-2.5, -1, 0]),
            MathTex(r"\beta").move_to([2.5, -1, 0]),
            MathTex(r"\gamma").move_to([0, 1.5, 0])
        )
        
        # Create the equation
        equation = MathTex(r"\alpha", "+", r"\beta", "+", r"\gamma", "=", "180°").to_edge(DOWN)
        
        # Add triangle and labels to the scene
        self.play(Create(triangle))
        self.play(Write(labels))
        
        # Calculate angles and create arcs
        vertices = triangle.get_vertices()
        angles = []
        arcs = []
        colors = [RED, GREEN, BLUE]
        for i in range(3):
            v1 = vertices[(i+1)%3] - vertices[i]
            v2 = vertices[(i-1)%3] - vertices[i]
            angle = self.angle_between_vectors(v1, v2)
            angles.append(angle)
            
            # Create arc
            arc = Arc(radius=0.5, angle=angle, color=colors[i])
            arc.move_arc_center_to(vertices[i])
            
            # Rotate arc to align with angle
            rotation_angle = self.angle_of_vector(v1)
            arc.rotate(rotation_angle, about_point=vertices[i])
            
            # Adjust arc position
            arc.shift(vertices[i] - arc.get_center())
            
            arcs.append(arc)

        # Highlight each angle and add it to the equation
        for i, (angle, arc) in enumerate(zip(angles, arcs)):
            self.play(Create(arc))
            self.play(labels[i].animate.set_color(colors[i]))
            self.play(TransformFromCopy(labels[i], equation[2*i]))
            
            if i < 2:
                self.play(Write(equation[2*i+1]))  # Write the "+" sign
        
        # Complete the equation
        self.play(Write(equation[5:]))
        
        # Move angles to form a straight line
        angle_copies = VGroup(*[arc.copy() for arc in arcs])
        self.play(FadeIn(angle_copies))
        
        target_angles = VGroup(
            angle_copies[0].copy().move_to([-2, -3, 0]),
            angle_copies[1].copy().next_to(angle_copies[0], RIGHT, buff=0),
            angle_copies[2].copy().next_to(angle_copies[1], RIGHT, buff=0)
        )
        
        self.play(
            *[Transform(angle_copies[i], target_angles[i]) for i in range(3)],
            run_time=2
        )
        
        # Show the straight line
        line = Line(start=angle_copies[0].get_left(), end=angle_copies[2].get_right(), color=YELLOW)
        self.play(Create(line))
        
        # Final emphasis
        self.play(equation.animate.scale(1.5))
        self.wait(2)
        
        # Show rotation
        self.play(Rotate(triangle, angle=2*PI, about_point=triangle.get_center()), run_time=4)
        self.wait(1)

    def angle_between_vectors(self, v1, v2):
        return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def angle_of_vector(self, v):
        return np.arctan2(v[1], v[0])
