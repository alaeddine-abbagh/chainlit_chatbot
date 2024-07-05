from manim import *
import random
import networkx as nx

class CubeAntsAnimation(ThreeDScene):
    def construct(self):
        # Create a 3D cube with edge length 3
        cube = Cube(side_length=3, fill_opacity=0.2, stroke_width=3)
        
        # Define the vertices of the cube
        vertices = [
            cube.get_corner(UP + LEFT + OUT),
            cube.get_corner(UP + RIGHT + OUT),
            cube.get_corner(DOWN + RIGHT + OUT),
            cube.get_corner(DOWN + LEFT + OUT),
            cube.get_corner(UP + LEFT + IN),
            cube.get_corner(UP + RIGHT + IN),
            cube.get_corner(DOWN + RIGHT + IN),
            cube.get_corner(DOWN + LEFT + IN)
        ]
        
        # Define the edges of the cube
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        
        # Create a graph for pathfinding
        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)
        
        # Place 8 ants on the vertices with different colors
        ant_colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
        ants = VGroup(*[
            Sphere(radius=0.15, fill_color=color, fill_opacity=0.8, stroke_width=0)
            .add(Sphere(radius=0.2, fill_color=color, fill_opacity=0.3, stroke_width=0))  # Add glow effect
            for color in ant_colors
        ])
        
        # Place ants on random edges
        for ant in ants:
            edge = random.choice(cube.edges)
            ant.move_to(edge.get_center())
        
        # Add cube to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(cube)
        
        # Animate the cube rotation
        self.play(Rotate(cube, angle=2*PI, axis=UP, run_time=2))
        self.wait(1)
        
        # Add ants after the cube stops rotating
        self.play(FadeIn(ants))
        self.wait(1)
        
        # Showcase the distance between two ants twice
        for _ in range(2):
            # Select two random ants
            ant1, ant2 = random.sample(list(ants), 2)
            
            # Highlight the selected ants
            self.play(
                ant1.animate.scale(1.5),
                ant2.animate.scale(1.5)
            )
            
            # Highlight the edge between the ants
            highlighted_edge = Line(ant1.get_center(), ant2.get_center(), color=YELLOW, stroke_width=5)
            
            # Calculate distance
            distance = np.linalg.norm(ant1.get_center() - ant2.get_center())
            distance_label = Text(f"Distance: {distance:.2f}", font_size=24).to_corner(UL)
            
            self.add(distance_label)
            self.play(Create(highlighted_edge), run_time=2)
            self.wait(1)
            
            # Reset for next iteration
            self.play(
                ant1.animate.scale(1/1.5),
                ant2.animate.scale(1/1.5),
                FadeOut(highlighted_edge),
                FadeOut(distance_label)
            )
            
            # Move ants to new random edges between iterations
            if _ == 0:
                self.play(*[
                    ant.animate.move_to(random.choice(cube.edges).get_center())
                    for ant in ants
                ])
    
    # Remove unused methods

# The file now ends here, removing the if __name__ == "__main__": block
