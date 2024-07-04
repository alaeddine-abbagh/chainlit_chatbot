from manim import *
import random

class CubeAntsAnimation(ThreeDScene):
    def construct(self):
        # Create a 3D cube with edge length 1
        cube = Cube(side_length=1, fill_opacity=0.1, stroke_width=2)
        
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
        
        # Place 8 ants randomly on the edges
        ants = VGroup(*[Dot(self.random_point_on_edge(vertices, edges), color=RED, radius=0.05) for _ in range(8)])
        
        # Add cube and ants to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(cube, ants)
        self.wait(1)
        
        # Repeat the process of highlighting paths between random pairs of ants
        for _ in range(3):
            # Select two random ants
            ant1, ant2 = random.sample(list(ants), 2)
            
            # Highlight the selected ants
            self.play(
                ant1.animate.set_color(YELLOW).scale(1.5),
                ant2.animate.set_color(YELLOW).scale(1.5)
            )
            
            # Find and highlight the shortest path
            path = self.find_shortest_path(vertices, edges, ant1, ant2)
            path_obj = VMobject()
            path_obj.set_points_smoothly([vertices[i] for i in path])
            
            distance_counter = DecimalNumber(0, num_decimal_places=2).to_corner(UR)
            distance_label = Text("Distance: ").next_to(distance_counter, LEFT)
            self.add(distance_counter, distance_label)
            
            def update_counter(mob):
                mob.set_value(path_obj.get_length())
            
            distance_counter.add_updater(update_counter)
            
            self.play(Create(path_obj), run_time=2)
            self.wait(1)
            
            # Reset for next iteration
            self.play(
                ant1.animate.set_color(RED).scale(1/1.5),
                ant2.animate.set_color(RED).scale(1/1.5),
                FadeOut(path_obj),
                FadeOut(distance_counter),
                FadeOut(distance_label)
            )
    
    def random_point_on_edge(self, vertices, edges):
        edge = random.choice(edges)
        t = random.random()
        return vertices[edge[0]] * (1 - t) + vertices[edge[1]] * t
    
    def find_shortest_path(self, vertices, edges, start, end):
        # Implement Dijkstra's algorithm or A* to find the shortest path
        # This is a simplified version that just returns a direct path
        start_index = min(range(len(vertices)), key=lambda i: np.linalg.norm(start.get_center() - vertices[i]))
        end_index = min(range(len(vertices)), key=lambda i: np.linalg.norm(end.get_center() - vertices[i]))
        return [start_index, end_index]

if __name__ == "__main__":
    scene = CubeAntsAnimation()
    scene.render()
