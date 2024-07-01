from manim import *

class CircleBisectorAnimation(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(radius=2, color=BLUE)
        
        # Create the bisector line
        bisector = Line(start=circle.get_left(), end=circle.get_right(), color=RED)
        
        # Add circle to the scene
        self.play(Create(circle))
        
        # Add bisector to the scene
        self.play(Create(bisector))
        
        # Wait for a moment
        self.wait(2)
