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
        
        # Place 12 ants on the edges (one per edge) with different colors
        ant_colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL, MAROON, GOLD, LIGHT_BROWN, GRAY]
        ants = VGroup(*[
            Dot(self.point_on_edge(vertices, edge), color=color, radius=0.1)
            .add(Dot(radius=0.15, color=color, fill_opacity=0.3))  # Add glow effect
            for edge, color in zip(edges, ant_colors)
        ])
        
        # Add cube to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(cube)
        
        # Animate the cube rotation
        self.play(Rotate(cube, angle=2*PI, axis=UP, run_time=2))
        self.wait(1)
        
        # Add ants after the cube stops rotating
        self.play(FadeIn(ants))
        self.wait(1)
        
        # Repeat the process of highlighting paths from a random ant to its closest neighbor
        for _ in range(3):
            # Select a random ant
            ant1 = random.choice(ants)
            
            # Find the closest ant
            ant2, path = self.find_closest_ant(vertices, edges, ant1, ants)
            
            # Highlight the selected ants
            self.play(
                ant1.animate.scale(1.5),
                ant2.animate.scale(1.5)
            )
            
            # Highlight the shortest path
            highlighted_edges = VGroup(*[Line(vertices[path[i]], vertices[path[i+1]], color=YELLOW, stroke_width=5) for i in range(len(path)-1)])
            
            distance = self.calculate_path_distance(vertices, path)
            distance_label = Text(f"Distance to closest: {distance:.2f}", font_size=24).to_corner(UL)
            self.add(distance_label)
            
            self.play(Create(highlighted_edges), run_time=2)
            self.wait(1)
            
            # Reset for next iteration
            self.play(
                ant1.animate.scale(1/1.5),
                ant2.animate.scale(1/1.5),
                FadeOut(highlighted_edges),
                FadeOut(distance_label)
            )
    
    def point_on_edge(self, vertices, edge):
        t = 0.5  # Place ant in the middle of the edge
        return vertices[edge[0]] * (1 - t) + vertices[edge[1]] * t
    
    def find_closest_ant(self, vertices, edges, start, ants):
        start_index = min(range(len(vertices)), key=lambda i: np.linalg.norm(start.get_center() - vertices[i]))
        min_distance = float('inf')
        closest_ant = None
        closest_path = None
        
        for ant in ants:
            if ant == start:
                continue
            end_index = min(range(len(vertices)), key=lambda i: np.linalg.norm(ant.get_center() - vertices[i]))
            path = nx.shortest_path(self.graph, start_index, end_index)
            distance = self.calculate_path_distance(vertices, path)
            if distance < min_distance:
                min_distance = distance
                closest_ant = ant
                closest_path = path
        
        return closest_ant, closest_path
    
    def calculate_path_distance(self, vertices, path):
        return sum(np.linalg.norm(vertices[path[i]] - vertices[path[i+1]]) for i in range(len(path)-1))

# The file now ends here, removing the if __name__ == "__main__": block
