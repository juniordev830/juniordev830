"""Testes do portfolio: evidencias verificaveis sem progresso inventado."""
import unittest
from xml.etree import ElementTree
from scripts.render_portfolio_progress import stage, summaries, render_svg, render_report, replace_section, START, END, collect


def sample(name, docs=True, code=True, tests=False, ci=False, pushed="2026-11-12", archived=False, partial=False):
    return dict(name=name, url="https://github.com/juniordev830/" + name,
                pushed=pushed, docs=docs, code=code, tests=tests, ci=ci,
                archived=archived, partial=partial)


class PortfolioProgressTests(unittest.TestCase):
    def test_technical_stages_are_not_completion_percentages(self):
        self.assertEqual(stage(sample("a", tests=True, ci=True)), "Validacao automatizada")
        self.assertEqual(stage(sample("a", tests=True)), "Com testes")
        self.assertEqual(stage(sample("a")), "Implementacao")
        self.assertEqual(stage(sample("a", code=False)), "Estruturacao")
        self.assertEqual(stage(sample("a", code=False, docs=False)), "Sem evidencias")
        self.assertEqual(stage(sample("a", partial=True)), "Inspecao parcial")

    def test_svg_valid_and_counted_only_from_records(self):
        projects = [sample("foo", ci=True, tests=True), sample("bar", code=False)]
        svg = render_svg(projects)
        ElementTree.fromstring(svg)
        self.assertIn("Com testes", svg)
        self.assertIn("ULTIMAS MOVIMENTACOES", svg)
        self.assertNotIn("72%", svg)
        self.assertEqual(summaries(projects)["validated"], 1)

    def test_report_has_every_repo_and_methods(self):
        projects = [sample("foo"), sample("bar", tests=True)]
        report = render_report(projects)
        self.assertEqual(report.count("github.com/juniordev830/"), 2)
        self.assertIn("Metodologia", report)
        self.assertIn("nao equivale", report)

    def test_preserves_rest_of_profile_and_rejects_bad_markers(self):
        original = "topo\n" + START + "\nold\n" + END + "\nrodape"
        replacement = replace_section(original, "NEW")
        self.assertEqual(replacement, "topo\n" + START + "\n\nNEW\n\n" + END + "\nrodape")
        with self.assertRaises(ValueError):
            replace_section("without markers", "NEW")

    def test_restricted_repositories_are_not_misclassified_as_empty(self):
        restricted = sample("codvision", docs=False, code=False, partial=True)
        restricted["restricted"] = True
        public = sample("publico", tests=True, ci=True)
        self.assertEqual(stage(restricted), "Acesso restrito")
        overview = summaries([restricted, public])
        self.assertEqual((overview["repos"], overview["scanned"], overview["restricted"]), (2, 1, 1))
        report = render_report([restricted, public])
        self.assertIn("N/D", report)
        self.assertIn("Auditados: 1", report)

    def test_missing_token_prevents_invented_data(self):
        with self.assertRaises(ValueError):
            collect("")


if __name__ == "__main__":
    unittest.main()
