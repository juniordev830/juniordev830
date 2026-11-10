"""Testes do painel: dados reais, sem preencher dias ausentes artificialmente."""
import unittest
from datetime import date, datetime, timedelta, timezone
from xml.etree import ElementTree

from scripts.render_daily_contributions import metrics, render_svg, fetch_calendar


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


if __name__ == "__main__":
    unittest.main()
