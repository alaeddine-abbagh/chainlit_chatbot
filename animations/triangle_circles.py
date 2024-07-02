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
        Q = C + (A - C) * 0.35
        R = A + (B - A) * 0.60
        points = VGroup(
            Dot(P, color=YELLOW),
            Dot(Q, color=YELLOW),
            Dot(R, color=YELLOW)
        )
        point_labels = VGroup(
            MathTex("P").next_to(P, UP+ 2*RIGHT, buff=0.2),
            MathTex("Q").next_to(Q, UP+LEFT, buff=0.2),
            MathTex("R").next_to(R, 2*DOWN, buff=0.2)
        )
        
        # Create circles
        circle_AQR = Circle.from_three_points(A, Q, R, color=YELLOW)
        circle_BRP = Circle.from_three_points(B, R, P, color=PINK)
        circle_CPQ = DashedVMobject(Circle.from_three_points(C, P, Q, color=ORANGE), num_dashes=50)
        
        # Find intersection point X
        def circle_intersection(circle1, circle2):
            center1, radius1 = circle1.get_center(), circle1.radius
            center2, radius2 = circle2.get_center(), circle2.radius
            d = np.linalg.norm(center1 - center2)
            a = (radius1**2 - radius2**2 + d**2) / (2*d)
            h = np.sqrt(radius1**2 - a**2)
            p = center1 + a * (center2 - center1) / d
            perp = np.array([-center2[1] + center1[1], center2[0] - center1[0], 0])
            X1 = p + h * perp / np.linalg.norm(perp)
            X2 = p - h * perp / np.linalg.norm(perp)
            # Return the point inside the triangle
            if np.dot(X1 - A, B - A) > 0 and np.dot(X1 - B, C - B) > 0 and np.dot(X1 - C, A - C) > 0:
                return X1
            return X2

        X = circle_intersection(circle_AQR, circle_BRP)
        point_X = Dot(X, color=YELLOW)
        label_X = MathTex("X").next_to(X, 2*DOWN+2*LEFT, buff=0.2)
        
                
        # Animation
        self.play(Create(triangle), run_time=1.5)
        self.play(Write(labels), run_time=1)
        self.wait(0.5)
        
        self.play(Create(points), run_time=1)
        self.play(Write(point_labels), run_time=1)
        self.wait(0.5)
        
        # Draw circles one by one
        for circle in [circle_AQR, circle_BRP]:
            self.play(Create(circle), run_time=2)
            self.wait(0.5)
        
        self.play(FadeIn(point_X), Write(label_X), run_time=1)
        self.wait(0.5)
        
        # Emphasize the question
        question = Text("Does X lie on circle CPQ?", font_size=32, color=ORANGE).to_edge(DOWN, buff=0.5)
        self.play(Write(question), run_time=1.5)
        self.wait(1)
        
        # Draw the dashed circle with emphasis
        self.play(Create(circle_CPQ), run_time=3)
        self.play(Indicate(circle_CPQ, color=ORANGE, scale_factor=1.3), run_time=2)
        self.wait(1)
        
        # Highlight that X is on all three circles
        self.play(
            circle_AQR.animate.set_stroke(width=6),
            circle_BRP.animate.set_stroke(width=6),
            circle_CPQ.animate.set_stroke(width=6),
            point_X.animate.scale(1.5),
            run_time=2
        )       
    
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
