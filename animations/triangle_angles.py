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
        
        # Calculate angles and create arcs
        vertices = triangle.get_vertices()
        angles = []
        arcs = []
        colors = [RED, GREEN, BLUE]
        for i in range(3):
            v1 = vertices[(i+1)%3] - vertices[i]
            v2 = vertices[(i-1)%3] - vertices[i]
            angle = np.arctan2(np.cross(v1, v2), np.dot(v1, v2))
            angle = abs(angle)  # Ensure positive angle
            angles.append(angle)
            
            # Create arc
            arc = Arc(radius=0.5, angle=angle, color=colors[i])
            arc.move_arc_center_to(vertices[i])
            
            # Rotate arc to align with angle
            rotation_angle = np.arctan2(v1[1], v1[0])
            arc.rotate(rotation_angle, about_point=vertices[i])
            if v1[0] * v2[1] - v1[1] * v2[0] < 0:
                arc.rotate(PI, about_point=vertices[i])
            
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
        
        # Final emphasis
        self.play(equation.animate.scale(1.5))
        self.wait(2)
