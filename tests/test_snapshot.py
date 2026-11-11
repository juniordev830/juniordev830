import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from scripts.render_daily_contributions import metrics, render_snapshot, render_svg, render_chart
from test_daily_contributions import fake_calendar, TODAY


class SnapshotTests(unittest.TestCase):
    def test_machine_snapshot_matches_calendar_exactly(self):
        data = metrics(fake_calendar(), TODAY)
        snapshot = json.loads(render_snapshot(data))
        self.assertEqual(snapshot['schemaVersion'], 1)
        self.assertEqual(snapshot['user'], 'juniordev830')
        self.assertEqual(snapshot['stats'], {'today':13,'yesterday':12,'week':70,'year':2012})
        self.assertEqual([day['count'] for day in snapshot['days']], list(range(14)))
        self.assertEqual(snapshot['dailyGoal'], 250)
        self.assertEqual(snapshot['observedOn'], TODAY.isoformat())
        self.assertEqual(snapshot['goalProgress'], {
            'remainingToday': 237,
            'reachedToday': False,
            'percentToday': 5.2,
        })

    def test_goal_progress_reflects_overachievement_without_capping(self):
        data = metrics(fake_calendar(), TODAY)
        data['today'] = 300
        data['counts'][-1] = 300
        progress = json.loads(render_snapshot(data))['goalProgress']
        self.assertEqual(progress, {
            'remainingToday': 0,
            'reachedToday': True,
            'percentToday': 120.0,
        })
        data['today'] = 250
        data['counts'][-1] = 250
        self.assertEqual(
            json.loads(render_snapshot(data))['goalProgress']['remainingToday'], 0,
        )

    def test_snapshot_changes_when_calendar_day_changes(self):
        data = metrics(fake_calendar(), TODAY)
        original = json.loads(render_snapshot(data))
        data['days'] = [day + timedelta(days=1) for day in data['days']]
        updated = json.loads(render_snapshot(data))
        self.assertEqual(original['observedOn'], TODAY.isoformat())
        self.assertEqual(updated['observedOn'], (TODAY + timedelta(days=1)).isoformat())
        self.assertEqual(updated['days'][-1]['date'], updated['observedOn'])
        self.assertNotEqual(original['observedOn'], updated['observedOn'])

    def test_percentage_and_chart_goal_use_250(self):
        data = metrics(fake_calendar(), TODAY)
        svg = render_svg(data, datetime(2026,11,10,tzinfo=timezone.utc))
        self.assertIn('>5%</text>', svg)
        self.assertIn('Referência: 250/dia', svg)
        self.assertIn('meta de 250/dia', svg)
        self.assertNotIn('meta de 100', svg)

    def test_goal_change_invalidates_image_cache(self):
        data = metrics(fake_calendar(), TODAY)
        before = render_chart(data)
        with patch('scripts.render_daily_contributions.DAILY_GOAL',300):
            self.assertNotEqual(render_chart(data),before)

    def test_snapshot_serialization_is_deterministic(self):
        data = metrics(fake_calendar(), TODAY)
        self.assertEqual(render_snapshot(data),render_snapshot(data))
        self.assertNotIn('generatedAt',render_snapshot(data))
