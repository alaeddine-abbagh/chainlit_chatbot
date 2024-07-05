from manim import *
import os

class BinomialTheoremAnimation(Scene):
    def construct(self):
        # Load the pop sound
        pop_sound = os.path.join(os.path.dirname(__file__), "pop_sound.wav")
        # # Set a gradient background
        # background = Rectangle(width=config.frame_width, height=config.frame_height, fill_opacity=1)
        # background.set_color(color=[BLUE_E, PURPLE_E])
        # self.add(background)

        # Title screen with animated text
        title = Text("The Binomial Theorem", font_size=72, color=YELLOW)
        self.play(AddTextWordByWord(title, run_time=1.5))
        self.wait(1)
        self.play(FadeOut(title, shift=UP))

        # General form of the Binomial Theorem with animated parts
        general_form = MathTex(
            r"(a + b)^n = \sum_{k=0}^n ", r"C_n^k", r"a^{n-k}b^k",
            font_size=60
        )
        general_form[0].set_color(BLUE)
        general_form[1].set_color(RED)
        general_form[2].set_color(GREEN)
        
        self.play(Write(general_form[0]))
        self.play(FadeIn(general_form[1], shift=DOWN))
        self.play(FadeIn(general_form[2], shift=RIGHT))
        self.wait(1)
        self.play(general_form.animate.to_edge(UP))

        # Add explanation for C_n^k with animated reveal
        explanation = MathTex(
            r"C_n^k = \binom{n}{k} = \frac{n!}{k!(n-k)!}",
            font_size=48
        ).set_color(YELLOW)
        explanation.next_to(general_form, 3*DOWN, buff=0.5)

        text_overlay = Text("The hard way", font_size=36, color=RED)
        text_overlay.next_to(explanation, 1.5*DOWN)
        self.play(FadeIn(text_overlay))
        self.wait(1)
        self.play(Write(explanation, run_time=1.5))
        self.wait(1)
        
        # Add text overlay
       
        self.play(FadeOut(explanation), FadeOut(text_overlay))

        # Pascal's Triangle with more vibrant colors
        pascal_triangle = VGroup()
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        for i in range(5):
            row = VGroup()
            for j in range(i + 1):
                if j == 0 or j == i:
                    num = 1
                else:
                    num = pascal_triangle[i-1][j-1].number + pascal_triangle[i-1][j].number
                cell = Integer(num, color=colors[i]).scale(0.9)
                row.add(cell)
            row.arrange(RIGHT, buff=0.7)
            pascal_triangle.add(row)
        pascal_triangle.arrange(DOWN, buff=0.7, center=False)
        pascal_triangle.next_to(general_form, DOWN, buff=0.7)

        # Text overlay for Pascal's Triangle
        pascal_text = Text("The easy way", font_size=36, color=GREEN)
        pascal_text.next_to(general_form, DOWN)

        # Animate Pascal's Triangle construction with faster pace
        self.play(FadeIn(pascal_text))
        self.play(FadeOut(pascal_text))
        # Initial zoom out
        self.play(pascal_triangle.animate.scale(0.7).to_edge(DOWN), run_time=1)

        self.play(FadeIn(pascal_triangle[0]))
        for i in range(1, 5):
            self.play(FadeIn(pascal_triangle[i]), run_time=0.5)
            
            # Zoom in for each new row
            self.play(pascal_triangle.animate.scale(1.1).move_to(ORIGIN), run_time=0.5)
            
            for j in range(1, i):
                self.play(
                    Indicate(pascal_triangle[i-1][j-1], color=WHITE, scale_factor=1.4),
                    Indicate(pascal_triangle[i-1][j], color=WHITE, scale_factor=1.4),
                    run_time=0.4
                )
                self.add_sound(pop_sound)
                self.play(
                    Indicate(pascal_triangle[i][j], color=PINK, scale_factor=1.8),
                    run_time=0.3
                )
                self.play(
                    pascal_triangle[i-1][j-1].animate.set_color(colors[i-1]),
                    pascal_triangle[i-1][j].animate.set_color(colors[i-1]),
                    pascal_triangle[i][j].animate.set_color(colors[i]),
                    run_time=0.4
                )
            
            # Zoom out after completing each row
            if i < 4:
                self.play(pascal_triangle.animate.scale(0.9).to_edge(DOWN), run_time=0.5)

        # Final zoom out to show the entire triangle
        self.play(pascal_triangle.animate.scale(0.8).to_edge(DOWN), run_time=1)
        self.wait(1)

        # Relationship between coefficients and Pascal's Triangle
        self.play(FadeOut(pascal_triangle[0], pascal_triangle[1], pascal_triangle[2], pascal_triangle[3]))
        fourth_row = pascal_triangle[4]
        self.play(fourth_row.animate.next_to(general_form, DOWN, buff=1))

        expansion = MathTex(
            r"(a+b)^4 = 1a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + 1b^4",
            font_size=48
        ).next_to(fourth_row, DOWN, buff=0.5)

        # Text overlay for expansion
      

        self.play(Write(expansion))
        coefficient_indices = [7, 11, 16, 22, 27]  # Indices of the coefficients in the expansion
        for i, index in enumerate(coefficient_indices):
            self.add_sound(pop_sound)
            self.play(
                Indicate(fourth_row[i], color=PINK, scale_factor=1.5),
                Indicate(expansion[0][index], color=PINK, scale_factor=1.5),
                run_time=0.6
            )
        self.wait(1)

        # Final message
        final_message = Text("Master the Binomial Theorem!", font_size=48, color=YELLOW)
        final_message.move_to(ORIGIN)

        self.play(FadeOut(general_form, fourth_row, expansion))
        self.play(Write(final_message))
        self.wait(1)

        # Add a pulsing effect to the final message
        self.play(
            Indicate(final_message, color=RED, scale_factor=1.2),
            rate_func=there_and_back,
            run_time=2
        )
        self.wait(1)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1920  # Changed to vertical video format
    config.pixel_width = 1080
    config.frame_rate = 60
    from manim.__main__ import main
    main()
