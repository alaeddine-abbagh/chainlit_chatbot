from manim import *
import random
import networkx as nx
from typing import List, Tuple

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
        
        # Calculate edge centers
        edge_centers = [
            (vertices[i] + vertices[j]) / 2 for i, j in edges
        ]
        
        # Place ants on random edge centers
        for ant in ants:
            ant.move_to(random.choice(edge_centers))
        
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
            
            # Find the shortest path between the ants
            path = self.find_shortest_path(ant1, ant2, vertices, edge_centers)
            
            # Highlight the edges in the path
            highlighted_edges = self.highlight_path(path, vertices)
            
            # Calculate distance
            distance = self.calculate_path_distance(path, vertices)
            distance_label = Text(f"Distance: {distance:.2f}", font_size=24).to_corner(UL)
            
            self.add(distance_label)
            if highlighted_edges:
                self.play(*[Create(edge) for edge in highlighted_edges], run_time=2)
            self.wait(1)
            
            # Reset for next iteration
            animations = [
                ant1.animate.scale(1/1.5),
                ant2.animate.scale(1/1.5),
                FadeOut(distance_label)
            ]
            if highlighted_edges:
                animations.extend([FadeOut(edge) for edge in highlighted_edges])
            self.play(*animations)
            
            # Move ants to new random edge centers between iterations
            if _ == 0:
                self.play(*[
                    ant.animate.move_to(random.choice(edge_centers))
                    for ant in ants
                ])
    
    def find_shortest_path(self, ant1: Mobject, ant2: Mobject, vertices: List[np.ndarray], edge_centers: List[np.ndarray]) -> List[int]:
        # Find the closest vertices to the ants
        start = min(range(len(vertices)), key=lambda i: np.linalg.norm(ant1.get_center() - vertices[i]))
        end = min(range(len(vertices)), key=lambda i: np.linalg.norm(ant2.get_center() - vertices[i]))
        
        # Find the shortest path using networkx
        return nx.shortest_path(self.graph, start, end)

    def highlight_path(self, path: List[int], vertices: List[np.ndarray]) -> List[Line]:
        highlighted_edges = []
        for i in range(len(path) - 1):
            start, end = vertices[path[i]], vertices[path[i+1]]
            edge = Line(start, end, color=YELLOW, stroke_width=5)
            highlighted_edges.append(edge)
        return highlighted_edges

    def calculate_path_distance(self, path: List[int], vertices: List[np.ndarray]) -> float:
        distance = 0
        for i in range(len(path) - 1):
            start, end = vertices[path[i]], vertices[path[i+1]]
            distance += np.linalg.norm(end - start)
        return distance

# The file now ends here, removing the if __name__ == "__main__": block
