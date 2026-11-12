"""Testes do painel: dados reais, sem preencher dias ausentes artificialmente."""
import json
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree

from scripts.render_daily_contributions import (
    START, END, metrics, period_insights, render_svg, render_chart, render_feed, render_markdown, update_readme, fetch_calendar, main,
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
    def test_period_insights_preserve_totals_and_group_actual_weekdays(self):
        data = metrics(fake_calendar(), TODAY)
        result = period_insights(data)
        self.assertEqual(result['total'], 91)
        self.assertEqual(result['average'], 6.5)
        self.assertEqual(result['active_days'], 13)
        self.assertEqual(result['streak'], 13)
        self.assertEqual(result['peak_count'], 13)
        self.assertEqual(result['peak_day'], TODAY)
        self.assertEqual(result['weekdays'], [17,19,7,9,11,13,15])
        self.assertEqual(result['cumulative'][-1], 91)
        self.assertAlmostEqual(result['week_delta_percent'], 100 * (70-21) / 21)

    def test_empty_activity_and_streak_are_limited_to_observed_window(self):
        data = metrics(fake_calendar(), TODAY)
        data['counts'] = [0]*14
        result = period_insights(data)
        self.assertEqual(result['streak'], 0)
        self.assertEqual(result['total'], 0)
        self.assertIsNone(result['week_delta_percent'])
        data['counts'] = [1]*14
        self.assertEqual(period_insights(data)['streak'], 14)
        data['counts'][-3] = 0
        self.assertEqual(period_insights(data)['streak'], 2)

    def test_complete_dashboard_heatmap_and_accumulation_keep_source_values(self):
        data = metrics(fake_calendar(), TODAY)
        root = ElementTree.fromstring(render_svg(data, datetime(2026,11,10,tzinfo=timezone.utc)))
        cells = [e for e in root.iter() if 'data-heat-date' in e.attrib]
        self.assertEqual([int(e.attrib['data-heat-count']) for e in cells], data['counts'])
        self.assertEqual([e.attrib['data-heat-date'] for e in cells], [d.isoformat() for d in data['days']])
        cumulative = [int(e.attrib['data-cumulative']) for e in root.iter() if 'data-cumulative' in e.attrib]
        self.assertEqual(cumulative, [sum(range(i+1)) for i in range(14)])

    def test_portfolio_is_part_of_the_same_svg_as_contributions(self):
        data = metrics(fake_calendar(), TODAY)
        xml = render_svg(data, datetime(2026, 11, 10, tzinfo=timezone.utc))
        root = ElementTree.fromstring(xml)
        self.assertEqual(root.attrib["height"], "1084")
        for title in ("Projetos em destaque", "Plataforma de Recrutamento",
                      "Atlas Sentinela", "Controle de Gastos"):
            self.assertIn(title, xml)
        self.assertIn("Contribuições diárias", xml)
        self.assertNotIn("<image", xml)

    def test_portfolio_links_remain_accessible_but_collapsed(self):
        result = render_markdown(metrics(fake_calendar(), TODAY),
                                 datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertIn("<summary>Links dos projetos em destaque</summary>", result)
        self.assertIn("https://github.com/juniordev830/sentinel-atlas", result)
        self.assertEqual(result.count("<img"), 1)

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
        self.assertIn("VISÃO GERAL", output)
        self.assertIn("Últimos 14 dias", output)
        self.assertIn("10/11", output)
        self.assertIn(">13</text>", output)
        self.assertIn("Média (7 dias): 10,0", output)

    def test_missing_token_fails_before_network(self):
        with self.assertRaisesRegex(ValueError, "GITHUB_TOKEN"):
            fetch_calendar("")

    def test_summary_totals_use_disjoint_weeks_and_observed_days(self):
        data = metrics(fake_calendar(), TODAY)
        svg = render_svg(data, datetime(2026, 11, 10, tzinfo=timezone.utc))
        root = ElementTree.fromstring(svg)
        values = [e.attrib['data-summary-values'] for e in root.iter() if 'data-summary-values' in e.attrib]
        self.assertEqual(values, ['70,21', '0,14'])
        data['counts'] = [0] * 14
        output = render_svg(data, datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertNotIn('NaN', output)
        self.assertNotRegex(output, r'(?i)\b(?:nan|inf)\b')

    def test_json_feed_preserves_calendar_and_official_totals(self):
        data = metrics(fake_calendar(), TODAY)
        raw = render_feed(data)
        self.assertTrue(raw.endswith("\n"))
        feed = json.loads(raw)
        self.assertEqual(feed["source"], "github-contributions-graphql")
        self.assertEqual(feed["login"], "juniordev830")
        self.assertEqual(feed["timezone"], "America/Fortaleza")
        self.assertEqual(feed["calendar_date"], TODAY.isoformat())
        self.assertEqual(feed["today"], 13)
        self.assertEqual(feed["yesterday"], 12)
        self.assertEqual(feed["last_7_days"], 70)
        self.assertEqual(feed["last_12_months"], 2012)
        self.assertEqual(feed["last_14_days"], [
            {"date": day.isoformat(), "contributions": count}
            for day, count in zip(data["days"], data["counts"])
        ])
        self.assertEqual(render_feed(data), raw)

    def test_chart_cache_changes_when_annual_total_changes(self):
        data = metrics(fake_calendar(), TODAY)
        original = render_chart(data)
        data['year_total'] += 1
        self.assertNotEqual(original, render_chart(data))

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
        for forbidden in ("<svg", "<script", "<iframe", "```mermaid"):
            self.assertNotIn(forbidden, output)

    def test_refresh_does_not_change_unchanged_counts_during_same_day(self):
        data = metrics(fake_calendar(), TODAY)
        morning = render_markdown(data, datetime(2026, 11, 10, 12, tzinfo=timezone.utc))
        evening = render_markdown(data, datetime(2026, 11, 10, 22, tzinfo=timezone.utc))
        self.assertEqual(morning, evening)

    def test_duplicate_summary_stays_invisible_without_breaking_raw_dashboard_metrics(self):
        from html.parser import HTMLParser

        class VisibleText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.chunks = []

            def handle_data(self, text):
                self.chunks.append(text)

        output = render_markdown(metrics(fake_calendar(), TODAY),
                                 datetime(2026, 11, 10, 17, tzinfo=timezone.utc))
        self.assertIn('<!-- CONTRIBUTIONS:METRICS <strong>13</strong><strong>12</strong><strong>70</strong><strong>2.012</strong> -->', output)
        visible = VisibleText()
        visible.feed(output)
        self.assertNotIn('2.012', ''.join(visible.chunks))
        self.assertNotIn('<table', output)
        self.assertNotIn('Média dos últimos 7 dias:', output)
        self.assertIn('<img', output)

    def test_chart_keeps_all_dates_and_values_in_chronological_order(self):
        data = metrics(fake_calendar(), TODAY)
        root = ElementTree.fromstring(render_svg(data, datetime(2026, 11, 10, tzinfo=timezone.utc)))
        bars = [e for e in root.iter() if "data-date" in e.attrib]
        self.assertEqual([e.attrib["data-date"] for e in bars], [d.isoformat() for d in data["days"]])
        self.assertEqual([int(e.attrib["data-count"]) for e in bars], list(range(14)))
        self.assertNotIn("<script", ElementTree.tostring(root, encoding="unicode"))

    def test_chart_does_not_clip_peaks_or_create_a_degenerate_zero_axis(self):
        calendar = fake_calendar()
        for day in calendar["weeks"][0]["contributionDays"]:
            day["contributionCount"] = 0
        for peak in (0, 553, 10000):
            calendar["weeks"][0]["contributionDays"][-1]["contributionCount"] = peak
            svg = render_svg(metrics(calendar, TODAY), datetime(2026, 11, 10, tzinfo=timezone.utc))
            root = ElementTree.fromstring(svg)
            for e in root.iter():
                if e.attrib.get("data-chart-bar") == "true":
                    self.assertGreaterEqual(float(e.attrib["y"]), float(e.attrib["data-plot-top"]) - .01)
                    self.assertLessEqual(float(e.attrib["y"]) + float(e.attrib["height"]), float(e.attrib["data-plot-bottom"]) + .02)

    def test_chart_is_outside_the_collapsed_daily_table_and_cache_tracks_data(self):
        data = metrics(fake_calendar(), TODAY)
        output = render_markdown(data, datetime(2026, 11, 10, 17, tzinfo=timezone.utc))
        self.assertLess(output.index("<img"), output.index("<details>"))
        self.assertNotIn("```mermaid", output)
        chart = render_chart(data)
        self.assertEqual(chart, render_chart(data))
        data["counts"][-1] += 1
        self.assertNotEqual(chart, render_chart(data))

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

    def test_main_updates_both_chart_and_readme_and_leaves_unchanged_files_alone(self):
        with TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            chart = Path(directory) / "assets/chart.svg"
            feed = Path(directory) / "assets/chart.json"
            readme.write_text("perfil\n" + START + "\nanterior\n" + END)
            with patch("scripts.render_daily_contributions.README", readme), \
                 patch("scripts.render_daily_contributions.CHART", chart), \
                 patch("scripts.render_daily_contributions.DATA", feed), \
                 patch("scripts.render_daily_contributions.fetch_calendar", return_value=fake_calendar()), \
                 patch("scripts.render_daily_contributions.datetime") as clock:
                clock.now.return_value = datetime(2026, 11, 10, 17, tzinfo=timezone.utc)
                main()
                self.assertTrue(chart.exists())
                self.assertTrue(feed.exists())
                self.assertEqual(json.loads(feed.read_text(encoding="utf-8"))["today"], 13)
                self.assertIn("<img", readme.read_text())
                before = (readme.stat().st_mtime_ns, chart.stat().st_mtime_ns, feed.stat().st_mtime_ns)
                main()
                self.assertEqual(before, (readme.stat().st_mtime_ns, chart.stat().st_mtime_ns, feed.stat().st_mtime_ns))


if __name__ == "__main__":
    unittest.main()
