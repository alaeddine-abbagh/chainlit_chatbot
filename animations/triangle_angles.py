from manim import *

class TriangleAnglesSum(Scene):
    def construct(self):
        # Create a triangle
        triangle = Polygon([-3, -1.5, 0], [3, -1.5, 0], [0, 2, 0], color=WHITE)
        
        # Create labels for the angles
        labels = VGroup(
            MathTex("a").move_to([-2.5, -1, 0]),
            MathTex("b").move_to([2.5, -1, 0]),
            MathTex("c").move_to([0, 1.5, 0])
        )
        
        # Create the equation
        equation = MathTex("a", "+", "b", "+", "c", "=", "180°").to_edge(DOWN)
        
        # Add triangle and labels to the scene
        self.play(Create(triangle))
        self.play(Write(labels))
        
        # Calculate angles
        vertices = triangle.get_vertices()
        angles = []
        for i in range(3):
            v1 = vertices[i] - vertices[(i-1)%3]
            v2 = vertices[(i+1)%3] - vertices[i]
            angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            angles.append(angle)

        # Highlight each angle and add it to the equation
        for i, (angle, color) in enumerate(zip(angles, [RED, GREEN, BLUE])):
            arc = Arc(radius=0.5, angle=angle, color=color)
            arc.move_arc_center_to(vertices[i])
            
            self.play(Create(arc))
            self.play(labels[i].animate.set_color(color))
            self.play(TransformFromCopy(labels[i], equation[2*i]))
            
            if i < 2:
                self.play(Write(equation[2*i+1]))  # Write the "+" sign
        
        # Complete the equation
        self.play(Write(equation[5:]))
        
        # Final emphasis
        self.play(equation.animate.scale(1.5))
        self.wait(2)
