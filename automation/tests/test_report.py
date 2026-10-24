"""Unit tests for report.py: counts, reasons, and the reply rate per template."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import report  # noqa: E402


def row(action, name="Rufus Pouros", live=True, reason="", template=None):
    return {"ts": "2026-10-25T10:00:00+08:00", "action": action, "live": live, "profile": {"name": name}, "reason": reason, "template_id": template, "text": None}


class SummaryTests(unittest.TestCase):
    def test_counts_and_reasons(self):
        rows = [row("like"), row("like", "B"), row("pass", "C", reason="age_below"), row("pass", "D", reason="age_below"), row("pass", "E", reason="gender"),
                row("message", template="t1"), row("message", "B", template="t2"), row("like", "Z", live=False), row("pass", "Y", live=False, reason="age_above")]
        s = report.summarise(rows)
        self.assertEqual((s["likes"], s["passes"], s["messages"], s["dry_run_actions"]), (2, 4, 2, 2))
        self.assertEqual(s["pass_reasons"], {"age_below": 2, "gender": 1, "age_above": 1})

    def test_reply_rate_per_template_counts_each_conversation_once(self):
        rows = [row("message", "A", template="t1"), row("message", "B", template="t1"), row("message", "C", template="t2"),
                row("reply", "A", template="t1"), row("reply", "A", template="t1"), row("reply", "C", template="t2")]
        s = report.summarise(rows)
        self.assertEqual(s["templates"]["t1"], {"sent": 2, "replied": 1, "reply_rate": 0.5})
        self.assertEqual(s["templates"]["t2"], {"sent": 1, "replied": 1, "reply_rate": 1.0})
        self.assertEqual(s["replies"], 2)

    def test_a_reply_for_an_unknown_template_is_ignored(self):
        s = report.summarise([row("message", template="t1"), row("reply", template="gone")])
        self.assertEqual(s["templates"]["t1"]["replied"], 0)

    def test_empty_ledger(self):
        s = report.summarise([])
        self.assertEqual((s["likes"], s["messages"], s["templates"]), (0, 0, {}))
        self.assertIn("Likes sent: 0", report.render_markdown(s))

    def test_markdown_table(self):
        md = report.render_markdown(report.summarise([row("message", template="t1"), row("reply", template="t1"), row("pass", "C", reason="gender")]))
        self.assertIn("| t1 | 1 | 1 | 100% |", md)
        self.assertIn("- gender: 1", md)


if __name__ == "__main__":
    unittest.main()
