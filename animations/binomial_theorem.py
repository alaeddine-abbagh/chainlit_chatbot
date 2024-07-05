from manim import *

class BinomialTheoremAnimation(Scene):
    def construct(self):
        # Title screen
        title = Text("The Binomial Theorem", font_size=60)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # General form of the Binomial Theorem
        general_form = MathTex(
            r"(a + b)^n = \sum_{k=0}^n ", r"C_n^k", r"a^{n-k}b^k",
            font_size=48
        )
        general_form[0].set_color(BLUE)
        general_form[1].set_color(RED)
        general_form[2].set_color(GREEN)
        
        self.play(Write(general_form))
        self.wait(2)
        self.play(general_form.animate.to_edge(UP))

        # Add explanation for C_n^k
        explanation = MathTex(
            r"C_n^k = \binom{n}{k} = \frac{n!}{k!(n-k)!}",
            font_size=36
        ).set_color(YELLOW)
        explanation.next_to(general_form, DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(2)
        self.play(FadeOut(explanation))

        # Pascal's Triangle
        pascal_triangle = VGroup()
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
        for i in range(5):
            row = VGroup()
            for j in range(i + 1):
                if j == 0 or j == i:
                    num = 1
                else:
                    num = pascal_triangle[i-1][j-1].number + pascal_triangle[i-1][j].number
                cell = Integer(num, color=colors[i]).scale(0.8)
                row.add(cell)
            row.arrange(RIGHT, buff=0.5)
            pascal_triangle.add(row)
        pascal_triangle.arrange(DOWN, buff=0.5, center=False)
        pascal_triangle.next_to(general_form, DOWN, buff=0.5)

        # Animate Pascal's Triangle construction
        self.play(FadeIn(pascal_triangle[0]))
        for i in range(1, 5):
            self.play(FadeIn(pascal_triangle[i]))
            for j in range(1, i):
                self.play(
                    Indicate(pascal_triangle[i-1][j-1], color=ORANGE, scale_factor=1.4),
                    Indicate(pascal_triangle[i-1][j], color=ORANGE, scale_factor=1.4),
                    run_time=0.8
                )
                self.play(
                    Indicate(pascal_triangle[i][j], color=YELLOW, scale_factor=1.8),
                    run_time=0.6
                )
                self.play(
                    pascal_triangle[i-1][j-1].animate.set_color(colors[i-1]),
                    pascal_triangle[i-1][j].animate.set_color(colors[i-1]),
                    pascal_triangle[i][j].animate.set_color(colors[i]),
                    run_time=0.8
                )
        self.wait(2)

        # Relationship between coefficients and Pascal's Triangle
        self.play(FadeOut(pascal_triangle[0], pascal_triangle[1], pascal_triangle[2], pascal_triangle[3]))
        fourth_row = pascal_triangle[4]
        self.play(fourth_row.animate.next_to(general_form, DOWN, buff=1))

        expansion = MathTex(
            r"(a+b)^4 = 1a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + 1b^4",
            font_size=36
        ).next_to(fourth_row, DOWN, buff=0.5)

        self.play(Write(expansion))
        coefficient_indices = [7, 11, 16, 22, 27]  # Indices of the coefficients in the expansion
        for i, index in enumerate(coefficient_indices):
            self.play(
                Indicate(fourth_row[i], color=ORANGE,scale_factor=1.5),
                Indicate(expansion[0][index], color=ORANGE, scale_factor=1.5),
                run_time=1
            )
        self.wait(2)

        # Focus on n = 3 case
        self.play(FadeOut(general_form, fourth_row, expansion))

        n3_case = MathTex(r"(a+b)^3", font_size=48)
        self.play(Write(n3_case))
        self.wait(1)

        expansion_steps = [
            MathTex(r"(a+b)^3 &= (a+b)(a+b)^2"),
            MathTex(r"&= (a+b)(a^2 + 2ab + b^2)"),
            MathTex(r"&= a(a^2 + 2ab + b^2) + b(a^2 + 2ab + b^2)"),
            MathTex(r"&= a^3 + 2a^2b + ab^2 + a^2b + 2ab^2 + b^3"),
            MathTex(r"&= a^3 + 3a^2b + 3ab^2 + b^3")
        ]

        for i, step in enumerate(expansion_steps):
            step.next_to(n3_case, DOWN, buff=0.5)
            if i == 0:
                self.play(Write(step))
            else:
                self.play(ReplacementTransform(expansion_steps[i-1], step))
            self.wait(1)

        self.wait(2)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    from manim.__main__ import main
    main()
