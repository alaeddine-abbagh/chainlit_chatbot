from manim import *
import numpy as np

class TriangleCircles(Scene):
    def construct(self):
        # Create the triangle ABC
        A = np.array([-3, -1.5, 0])
        B = np.array([3, -1.5, 0])
        C = np.array([0, 3, 0])
        triangle = Polygon(A, B, C, color=WHITE)
        
        # Create labels for the vertices
        labels = VGroup(
            MathTex("A").next_to(A, DOWN+LEFT, buff=0.2),
            MathTex("B").next_to(B, DOWN+RIGHT, buff=0.2),
            MathTex("C").next_to(C, UP, buff=0.2)
        )
        
        # Create points P, Q, R
        P = B + (C - B) * 0.6
        Q = C + (A - C) * 0.35  # Moved Q slightly towards C
        R = A + (B - A) * 0.65  # Moved R slightly towards A
        points = VGroup(
            Dot(P, color=RED),
            Dot(Q, color=GREEN),
            Dot(R, color=BLUE)
        )
        point_labels = VGroup(
            MathTex("P").next_to(P, RIGHT, buff=0.2),
            MathTex("Q").next_to(Q, UP+LEFT, buff=0.2),
            MathTex("R").next_to(R, DOWN+LEFT, buff=0.2)
        )
        
        # Create circles
        circle_AQR = Circle.from_three_points(A, Q, R, color=YELLOW)
        circle_BRP = Circle.from_three_points(B, R, P, color=PINK)
        circle_CPQ = DashedVMobject(Circle.from_three_points(C, P, Q, color=ORANGE), num_dashes=50)
        
        # Find intersection point X
        X = line_intersection(
            [circle_AQR.get_center(), circle_BRP.get_center()],
            [A, B]
        )
        point_X = Dot(X, color=PURPLE)
        label_X = MathTex("X").next_to(X, DOWN+RIGHT, buff=0.2)
        
        # Animation
        self.play(Create(triangle), Write(labels))
        self.play(Create(points), Write(point_labels))
        self.play(Create(circle_AQR), Create(circle_BRP))
        self.play(FadeIn(point_X), Write(label_X))
        self.play(Create(circle_CPQ))
        
        # Highlight that X is on all three circles
        self.play(
            circle_AQR.animate.set_stroke(width=6),
            circle_BRP.animate.set_stroke(width=6),
            circle_CPQ.animate.set_stroke(width=6),
            point_X.animate.scale(1.5),
            run_time=2
        )
        
        self.wait(2)

def line_intersection(line1, line2):
    x1, y1 = line1[0][:2]
    x2, y2 = line1[1][:2]
    x3, y3 = line2[0][:2]
    x4, y4 = line2[1][:2]
    
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None  # Lines are parallel
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1), 0])
