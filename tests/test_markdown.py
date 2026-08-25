import unittest

from dockit_fp.markdown import render_markdown


class MarkdownTests(unittest.TestCase):
    def test_renders_github_style_admonitions_without_the_bang(self) -> None:
        rendered = render_markdown("> [!IMPORTANT] Keep history accurate.", lambda target: target)

        self.assertIn('class="admonition important"', rendered.html)
        self.assertIn("<strong>Important</strong>", rendered.html)

    def test_marks_inline_display_and_fenced_math_for_katex(self) -> None:
        rendered = render_markdown(
            "Inline $x^2$\n\n$$\n\\int_0^1 x dx\n$$\n\n```math\n\\frac{a}{b}\n```",
            lambda target: target,
        )

        self.assertIn('class="math-inline" data-tex="x^2"', rendered.html)
        self.assertIn('class="math-display" data-tex="\\int_0^1 x dx"', rendered.html)
        self.assertIn('class="math-display" data-tex="\\frac{a}{b}"', rendered.html)
