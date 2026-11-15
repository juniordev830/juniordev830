"""Confere a navegação do mapa de projetos publicado no perfil."""
import re
import unittest
from pathlib import Path


README = Path(__file__).resolve().parents[1] / "README.md"
START = "<!-- PROJECT-MAP:START -->"
END = "<!-- PROJECT-MAP:END -->"


class ProjectMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        readme = README.read_text(encoding="utf-8")
        assert readme.count(START) == 1 and readme.count(END) == 1
        cls.section = readme.split(START, 1)[1].split(END, 1)[0]

    def test_seven_groups_and_seventeen_subgroups(self):
        # Sete áreas e dezessete subáreas, todas expansíveis.
        self.assertEqual(self.section.count("<details>"), 24)
        self.assertEqual(self.section.count("</details>"), 24)
        self.assertEqual(self.section.count("<summary>"), 24)
        self.assertEqual(len(re.findall(
            r"^<summary><strong>0[1-7] · ", self.section, flags=re.MULTILINE
        )), 7)
        self.assertEqual(len(re.findall(
            r"^<summary><strong>[^<]+</strong> · \d+ projetos?</summary>$",
            self.section, flags=re.MULTILINE
        )), 17)

    def test_group_counts_total_one_hundred(self):
        counts = [int(n) for n in re.findall(
            r"<summary>.*?— (\d+) projetos?", self.section
        )]
        self.assertEqual(len(counts), 7)
        self.assertEqual(sum(counts), 100)
        self.assertIn("98 projetos públicos e 2 privados", self.section)

    def test_links_are_valid_unique_and_public_count_is_consistent(self):
        urls = re.findall(
            r"\[[^\]\n]+\]\(https://github\.com/juniordev830/([^\)\n]+)\)",
            self.section,
        )
        self.assertEqual(len(urls), 98)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(self.section.count("*1 projeto privado*"), 2)


if __name__ == "__main__":
    unittest.main()
