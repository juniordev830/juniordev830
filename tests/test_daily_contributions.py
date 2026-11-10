"""Testes do painel: dados reais, sem preencher dias ausentes artificialmente."""
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree

from scripts.render_daily_contributions import (
    START, END, metrics, render_svg, render_markdown, update_readme, fetch_calendar, main,
)


TODAY = date(2026, 11, 10)


def fake_calendar(length=14):
    dates = [TODAY - timedelta(days=i) for i in range(length - 1, -1, -1)]
    return {
        "totalContributions": 2012,
        "weeks": [{"contributionDays": [
            {"date": day.isoformat(), "contributionCount": n}
            for n, day in enumerate(dates)
        ]}],
    }


class DashboardTests(unittest.TestCase):
    def test_exact_daily_counts_and_week_summary(self):
        result = metrics(fake_calendar(), TODAY)
        self.assertEqual(result["counts"], list(range(14)))
        self.assertEqual(result["today"], 13)
        self.assertEqual(result["yesterday"], 12)
        self.assertEqual(result["week_total"], sum(range(7, 14)))
        self.assertEqual(result["year_total"], 2012)
        self.assertAlmostEqual(result["week_average"], 10.0)

    def test_missing_days_are_not_silently_zeroed(self):
        with self.assertRaisesRegex(ValueError, "14 dias"):
            metrics(fake_calendar(13), TODAY)

    def test_invalid_counts_rejected(self):
        calendar = fake_calendar()
        calendar["weeks"][0]["contributionDays"][-1]["contributionCount"] = -1
        with self.assertRaisesRegex(ValueError, "inválida"):
            metrics(calendar, TODAY)

    def test_render_is_valid_svg_and_displays_every_count(self):
        result = metrics(fake_calendar(), TODAY)
        output = render_svg(result, datetime(2026, 11, 10, 17, tzinfo=timezone.utc))
        root = ElementTree.fromstring(output)
        self.assertTrue(root.tag.endswith("svg"))
        self.assertIn("Contribuições diárias", output)
        self.assertIn("Últimos 14 dias", output)
        self.assertIn("10/11", output)
        self.assertIn("2012", output.replace(".", ""))
        self.assertIn(">13</text>", output)
        self.assertIn("Média (7 dias): 10,0", output)

    def test_missing_token_fails_before_network(self):
        with self.assertRaisesRegex(ValueError, "GITHUB_TOKEN"):
            fetch_calendar("")

    def test_text_panel_includes_counts_and_expandable_daily_history(self):
        output = render_markdown(metrics(fake_calendar(), TODAY),
                                 datetime(2026, 11, 10, 17, tzinfo=timezone.utc))
        self.assertIn("<strong>13</strong>", output)
        self.assertIn("<strong>2.012</strong>", output)
        self.assertIn("<details>", output)
        self.assertIn("| 10/11/2026 | 13 |", output)
        self.assertIn("| 28/10/2026 | 0 |", output)
        self.assertLess(output.index("| 10/11/2026"), output.index("| 28/10/2026"))
        self.assertIn("5 minutos", output)
        for forbidden in ("<img", "<svg", "<script", "<iframe"):
            self.assertNotIn(forbidden, output)

    def test_refresh_does_not_change_unchanged_counts_during_same_day(self):
        data = metrics(fake_calendar(), TODAY)
        morning = render_markdown(data, datetime(2026, 11, 10, 12, tzinfo=timezone.utc))
        evening = render_markdown(data, datetime(2026, 11, 10, 22, tzinfo=timezone.utc))
        self.assertEqual(morning, evening)

    def test_replacement_preserves_everything_outside_the_panel(self):
        prefix = "# João Júnior\n\nTecnologias e projetos aprovados.\n\n"
        suffix = "\n\nExplore meu trabalho — links originais.\n"
        original = prefix + START + "\nold\n" + END + suffix
        updated = update_readme(original, "novo painel")
        self.assertEqual(updated, prefix + START + "\n\nnovo painel\n\n" + END + suffix)
        self.assertEqual(update_readme(updated, "novo painel"), updated)

    def test_ambiguous_or_missing_boundaries_are_rejected(self):
        for document in ("sem marcadores", START, END + START,
                         START + START + END, START + END + END):
            with self.subTest(document=document), self.assertRaises(ValueError):
                update_readme(document, "novo painel")

    def test_fetch_failure_never_replaces_the_previous_panel(self):
        with TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            original = "perfil aprovado\n" + START + "\nanterior\n" + END
            readme.write_text(original, encoding="utf-8")
            with patch("scripts.render_daily_contributions.README", readme), \
                 patch("scripts.render_daily_contributions.fetch_calendar", side_effect=ValueError("API indisponível")):
                with self.assertRaises(ValueError):
                    main()
            self.assertEqual(readme.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
