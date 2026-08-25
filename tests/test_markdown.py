import unittest

from dockit_fp.markdown import render_markdown


class MarkdownTests(unittest.TestCase):
    def test_renders_github_style_admonitions_without_the_bang(self) -> None:
        rendered = render_markdown("> [!IMPORTANT] Keep history accurate.", lambda target: target)

        self.assertIn('class="admonition important"', rendered.html)
        self.assertIn("<strong>Important</strong>", rendered.html)
