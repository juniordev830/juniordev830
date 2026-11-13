"""Testes do portfolio: evidencias verificaveis sem progresso inventado."""
import unittest
from xml.etree import ElementTree
from datetime import datetime, timezone, timedelta
from scripts.render_portfolio_progress import stage, summaries, render_svg, render_report, replace_section, START, END, collect, snapshot_marker


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
        self.assertIn("COM TESTES", svg)
        self.assertIn("Últimas movimentações", svg)
        self.assertNotIn("72%", svg)
        self.assertEqual(summaries(projects)["validated"], 1)

    def test_visual_redesign_preserves_true_evidence_counts(self):
        example = [
            sample("pixel-farm-seasons", tests=True, ci=True),
            sample("sentinel-atlas", tests=True, ci=True),
            sample("plataforma-de-recrutamento", code=True),
            sample("infrastructure-as-code-lab", code=True, tests=True),
        ]
        image = render_svg(example)
        root = ElementTree.fromstring(image)
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("Portfólio de", image)
        self.assertIn("Distribuição técnica", image)
        self.assertIn("Fluxo de evolução", image)
        self.assertIn("Últimas movimentações", image)
        self.assertIn("4/4 sinais técnicos", image)
        self.assertNotIn("70%", image)
        self.assertNotIn("<script", image)
        self.assertNotIn("<foreignObject", image)

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

    def test_snapshot_windows_are_six_hours_in_utc(self):
        self.assertEqual(snapshot_marker(datetime(2026, 11, 12, 5, 59, tzinfo=timezone.utc)),
                         "<!-- PORTFOLIO-SNAPSHOT:v4:2026-11-12T00Z -->")
        self.assertEqual(snapshot_marker(datetime(2026, 11, 12, 6, 0, tzinfo=timezone.utc)),
                         "<!-- PORTFOLIO-SNAPSHOT:v4:2026-11-12T06Z -->")
        self.assertEqual(snapshot_marker(datetime(2026, 11, 12, 21, tzinfo=timezone.utc)),
                         "<!-- PORTFOLIO-SNAPSHOT:v4:2026-11-12T18Z -->")
        self.assertEqual(snapshot_marker(datetime(2026, 11, 12, 16, tzinfo=timezone(timedelta(hours=-3)))),
                         "<!-- PORTFOLIO-SNAPSHOT:v4:2026-11-12T18Z -->")
        with self.assertRaises(ValueError):
            snapshot_marker(datetime(2026, 11, 12, 6))

    def test_missing_token_prevents_invented_data(self):
        with self.assertRaises(ValueError):
            collect("")


if __name__ == "__main__":
    unittest.main()
