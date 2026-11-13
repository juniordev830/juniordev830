"""Testes de consistência dos dois gráficos, README e JSON."""
import json
import unittest
from datetime import date, datetime, timedelta, timezone

from scripts.render_daily_contributions import render_feed, render_markdown, render_svg as render_daily
from scripts.render_portfolio_progress import render_svg as render_portfolio, render_report
from scripts.verify_profile_panels import verify


class PanelIntegrityTests(unittest.TestCase):
    def setUp(self):
        today = date(2026, 11, 12)
        days = [today - timedelta(days=i) for i in range(13, -1, -1)]
        counts = list(range(1, 15))
        data = {
            "days": days,
            "counts": counts,
            "today": counts[-1],
            "yesterday": counts[-2],
            "week_total": sum(counts[-7:]),
            "year_total": 2459,
            "week_average": sum(counts[-7:]) / 7,
        }
        self.readme = "<!-- CONTRIBUTIONS:START -->\n" + render_markdown(
            data, datetime(2026, 11, 12, tzinfo=timezone.utc)
        ) + "\n<!-- CONTRIBUTIONS:END -->\n"
        self.readme += '<img src="assets/portfolio-andamento.svg"/>'
        self.feed = json.loads(render_feed(data))
        self.daily_svg = render_daily(data, datetime(2026, 11, 12, tzinfo=timezone.utc))
        project = dict(name="demo", url="https://github.com/juniordev830/demo",
                       pushed="2026-11-12", pushed_iso="2026-11-12T15:00:00Z",
                       docs=True, code=True, tests=True, ci=True,
                       archived=False, partial=False)
        self.portfolio_svg = render_portfolio([project])
        self.report = "<!-- PORTFOLIO-SNAPSHOT:v4:2026-11-12T18Z -->\n" + render_report([project])

    def check(self):
        verify(self.readme, self.feed, self.daily_svg, self.portfolio_svg, self.report)

    def test_matching_panels_are_accepted(self):
        self.check()

    def test_wrong_feed_counts_are_rejected(self):
        self.feed["today"] = 999
        with self.assertRaisesRegex(ValueError, "JSON"):
            self.check()

    def test_outdated_readme_is_rejected(self):
        self.readme = self.readme.replace("<strong>14</strong>", "<strong>13</strong>")
        with self.assertRaisesRegex(ValueError, "README"):
            self.check()

    def test_missing_day_is_rejected(self):
        self.feed["last_14_days"][1]["date"] = "2026-11-12"
        with self.assertRaisesRegex(ValueError, "dias duplicados"):
            self.check()

    def test_inconsistent_svg_is_rejected(self):
        self.daily_svg = self.daily_svg.replace('data-count="14"', 'data-count="999"')
        with self.assertRaisesRegex(ValueError, "SVG"):
            self.check()

    def test_missing_portfolio_metadata_is_rejected(self):
        self.report = self.report.replace("PORTFOLIO-SNAPSHOT", "UNKNOWN-SNAPSHOT")
        with self.assertRaisesRegex(ValueError, "auditoria"):
            self.check()


if __name__ == "__main__":
    unittest.main()
