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
        
        # Place 8 ants randomly on the edges with different colors
        ant_colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
        ants = VGroup(*[Dot(self.random_point_on_edge(vertices, edges), color=color, radius=0.05) for color in ant_colors])
        
        # Add cube to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(cube)
        
        # Animate the cube rotation
        self.play(Rotate(cube, angle=2*PI, axis=UP, run_time=2))
        self.wait(1)
        
        # Add ants after the cube stops rotating
        self.play(FadeIn(ants))
        self.wait(1)
        
        # Repeat the process of highlighting paths between random pairs of ants
        for _ in range(3):
            # Select two random ants
            ant1, ant2 = random.sample(list(ants), 2)
            
            # Highlight the selected ants
            self.play(
                ant1.animate.scale(1.5),
                ant2.animate.scale(1.5)
            )
            
            # Find and highlight the shortest path
            path = self.find_shortest_path(vertices, edges, ant1, ant2)
            highlighted_edges = VGroup(*[Line(vertices[path[i]], vertices[path[i+1]], color=YELLOW, stroke_width=5) for i in range(len(path)-1)])
            
            distance = self.calculate_path_distance(vertices, path)
            distance_label = Text(f"Distance: {distance:.2f}", font_size=24).to_corner(UL)
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
    
    def random_point_on_edge(self, vertices, edges):
        edge = random.choice(edges)
        t = random.random()
        return vertices[edge[0]] * (1 - t) + vertices[edge[1]] * t
    
    def find_shortest_path(self, vertices, edges, start, end):
        start_index = min(range(len(vertices)), key=lambda i: np.linalg.norm(start.get_center() - vertices[i]))
        end_index = min(range(len(vertices)), key=lambda i: np.linalg.norm(end.get_center() - vertices[i]))
        return nx.shortest_path(self.graph, start_index, end_index)
    
    def calculate_path_distance(self, vertices, path):
        return sum(np.linalg.norm(vertices[path[i]] - vertices[path[i+1]]) for i in range(len(path)-1))

# The file now ends here, removing the if __name__ == "__main__": block
