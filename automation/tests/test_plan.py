"""Unit tests for plan.py: tables for every rule, then seeded random worlds for the rules that carry state (rotation, schedule, daily caps).

Run from the repo root: python -m unittest discover -s automation/tests -v
No browser, no network, no clock: every function takes its time and its random source from the test.
"""
import datetime as dt
import json
import os
import random
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import plan  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=8))
with open(os.path.join(HERE, "..", "automation.config.json"), encoding="utf-8") as _f:
    GOOD = json.load(_f)
FILTERS = GOOD["filters"]
TEMPLATES = GOOD["templates"]
PACING = {"min_gap_s": 20, "max_gap_s": 90, "active_hours": {"start": "09:00", "end": "22:00"}}


def profile(**kw):
    base = {"name": "Rufus Pouros", "first_name": "Rufus", "age": 37, "bio": "Mollitia excepturi voluptates", "city": "Demetricebury", "region": "Minnesota", "country": "Uruguay", "gender": "Male"}
    base.update(kw)
    return base


def at(hh, mm=0, day=25):
    return dt.datetime(2026, 10, day, hh, mm, tzinfo=TZ)


class ConfigTests(unittest.TestCase):
    def test_the_shipped_config_is_valid(self):
        self.assertEqual(plan.validate_config(GOOD), [])

    def test_every_broken_field_is_named(self):
        cases = {
            "base_url": (lambda c: c["app"].update(base_url="ftp://x"), "app.base_url"),
            "hosts": (lambda c: c["app"].update(allowed_hosts=[]), "allowed_hosts"),
            "minor": (lambda c: c["filters"].update(min_age=17), "min_age"),
            "age order": (lambda c: c["filters"].update(min_age=40, max_age=30), "max_age"),
            "genders": (lambda c: c["filters"].update(genders=[]), "genders"),
            "no templates": (lambda c: c.update(templates=[]), "templates"),
            "template without text": (lambda c: c["templates"].append({"id": "x"}), "id and a text"),
            "duplicate id": (lambda c: c["templates"].append(dict(c["templates"][0])), "used twice"),
            "unknown placeholder": (lambda c: c["templates"].append({"id": "n", "text": "Hi {nickname}"}), "{nickname}"),
            "gap order": (lambda c: c["pacing"].update(min_gap_s=100, max_gap_s=10), "pacing.min_gap_s"),
            "zero gap": (lambda c: c["pacing"].update(min_gap_s=0), "pacing.min_gap_s"),
            "hours order": (lambda c: c["pacing"]["active_hours"].update(start="22:00", end="09:00"), "active_hours"),
            "hours format": (lambda c: c["pacing"]["active_hours"].update(start="9am"), "active_hours"),
            "negative cap": (lambda c: c["caps"].update(likes_per_day=-1), "likes_per_day"),
            "cap type": (lambda c: c["caps"].update(messages_per_day="five"), "messages_per_day"),
            "run_at format": (lambda c: c["schedule"].update(run_at=["25:00"]), "run_at"),
        }
        for name, (mutate, needle) in cases.items():
            with self.subTest(name):
                cfg = json.loads(json.dumps(GOOD))
                mutate(cfg)
                problems = plan.validate_config(cfg)
                self.assertTrue(any(needle in p for p in problems), problems)

    def test_not_an_object(self):
        self.assertEqual(len(plan.validate_config([])), 1)

    def test_load_config_refuses_a_broken_file_and_reads_a_good_one(self):
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "bad.json")
            with open(bad, "w", encoding="utf-8") as f:
                json.dump({"app": {}}, f)
            with self.assertRaises(ValueError):
                plan.load_config(bad)
            self.assertEqual(plan.load_config(os.path.join(HERE, "..", "automation.config.json"))["caps"]["likes_per_day"], 8)


class HostTests(unittest.TestCase):
    def test_table(self):
        allowed = ["10.0.2.2", "localhost"]
        cases = [("http://10.0.2.2:5173/login", True), ("http://LOCALHOST/x", True), ("https://tinder.com/app", False), ("http://10.0.2.2.evil.com/", False),
                 ("http://evil.com/10.0.2.2", False), ("10.0.2.2", False), ("", False), ("http://user@evil.com:80@10.0.2.2/", False)]
        for url, ok in cases:
            with self.subTest(url):
                self.assertEqual(plan.host_allowed(url, allowed), ok)


class ProfileTests(unittest.TestCase):
    def test_a_card_is_read(self):
        p = plan.parse_profile({"name_text": "Rufus Pouros (37)", "bio": " hello there ", "gender_icon": "pi pi-mars gender-icon", "location": "Demetricebury, Minnesota, Uruguay"})
        self.assertEqual((p["name"], p["first_name"], p["age"], p["gender"], p["city"], p["region"], p["country"]), ("Rufus Pouros", "Rufus", 37, "Male", "Demetricebury", "Minnesota", "Uruguay"))
        self.assertEqual(p["bio"], "hello there")

    def test_a_country_with_a_comma_keeps_all_of_it(self):
        p = plan.parse_profile({"name_text": "A B (30)", "location": "X, Y, Slovakia, Republic"})
        self.assertEqual(p["country"], "Slovakia, Republic")

    def test_missing_parts_stay_empty_not_wrong(self):
        p = plan.parse_profile({"name_text": "Solo"})
        self.assertEqual((p["age"], p["gender"], p["city"], p["bio"]), (None, None, "", ""))
        self.assertIsNone(plan.parse_profile({"name_text": "Eve (x)"})["age"])

    def test_gender_icons(self):
        self.assertEqual(plan.parse_profile({"name_text": "A (30)", "gender_icon": "pi pi-venus gender-icon"})["gender"], "Female")
        self.assertIsNone(plan.parse_profile({"name_text": "A (30)", "gender_icon": "pi pi-star"})["gender"])


class DecideTests(unittest.TestCase):
    def test_table(self):
        cases = [
            (profile(), (True, "ok")),
            (profile(age=24), (False, "age_below")), (profile(age=25), (True, "ok")), (profile(age=45), (True, "ok")), (profile(age=46), (False, "age_above")),
            (profile(age=None), (False, "no_age")), (profile(gender="Female"), (False, "gender")), (profile(gender=None), (False, "gender")),
            (profile(bio=""), (False, "bio_missing")), (profile(bio="short"), (False, "bio_missing")),
            (profile(bio="a" * (FILTERS["min_bio_chars"] - 1)), (False, "bio_missing")), (profile(bio="a" * FILTERS["min_bio_chars"]), (True, "ok")), (profile(bio="Ask me about CRYPTO tips"), (False, "bio_blocked_word")),
        ]
        for prof, want in cases:
            with self.subTest(case=(prof["age"], prof["gender"], prof["bio"][:12])):
                self.assertEqual(plan.decide_profile(prof, FILTERS), want)

    def test_already_seen_wins_over_everything(self):
        self.assertEqual(plan.decide_profile(profile(age=99), FILTERS, seen={"Rufus Pouros"}), (False, "already_seen"))

    def test_no_genders_filter_means_any_gender(self):
        f = dict(FILTERS, genders=None)
        self.assertEqual(plan.decide_profile(profile(gender="Female"), f), (True, "ok"))

    def test_every_reason_is_a_known_one(self):
        rng = random.Random(3)
        for _ in range(500):
            p = profile(age=rng.choice([None, 10, 24, 25, 30, 45, 46, 80]), gender=rng.choice([None, "Male", "Female"]), bio=rng.choice(["", "x", "a long enough bio", "crypto fan here"]))
            self.assertIn(plan.decide_profile(p, FILTERS)[1], plan.REASONS)


class TemplateTests(unittest.TestCase):
    def test_render_fills_every_field(self):
        self.assertEqual(plan.render_template("Hi {first_name} from {city}, {age}", profile()), "Hi Rufus from Demetricebury, 37")

    def test_a_missing_field_is_an_error_not_a_hole(self):
        with self.assertRaises(ValueError):
            plan.render_template("Hi {first_name} in {city}", profile(city=""))

    def test_a_template_that_cannot_be_filled_is_skipped(self):
        choice = plan.choose_template(TEMPLATES, [], profile(city=""), random.Random(1))
        self.assertNotEqual(choice[0], "city-question")
        self.assertIsNone(plan.choose_template([{"id": "c", "text": "{city}"}], [], profile(city=""), random.Random(1)))

    def test_least_used_first_and_never_the_same_twice(self):
        rng = random.Random(5)
        for _ in range(300):
            history = [rng.choice([t["id"] for t in TEMPLATES]) for _ in range(rng.randint(0, 12))]
            tid, text = plan.choose_template(TEMPLATES, history, profile(), rng)
            counts = {t["id"]: history.count(t["id"]) for t in TEMPLATES}
            pool = [i for i in counts if i != (history[-1] if history else None)]
            self.assertEqual(counts[tid], min(counts[i] for i in pool))
            self.assertNotEqual(tid, history[-1] if history else None)
            self.assertNotIn("{", text)

    def test_long_run_stays_balanced(self):
        for seed in range(20):
            rng = random.Random(seed)
            history = []
            for _ in range(60):
                history.append(plan.choose_template(TEMPLATES, history, profile(), rng)[0])
            counts = [history.count(t["id"]) for t in TEMPLATES]
            self.assertLessEqual(max(counts) - min(counts), 1, (seed, counts))

    def test_a_single_template_may_repeat(self):
        one = TEMPLATES[:1]
        self.assertEqual(plan.choose_template(one, [one[0]["id"]], profile(), random.Random(1))[0], one[0]["id"])


class ScheduleTests(unittest.TestCase):
    def test_hours(self):
        a = PACING["active_hours"]
        self.assertTrue(plan.within_active_hours(at(9, 0), a))
        self.assertTrue(plan.within_active_hours(at(21, 59), a))
        self.assertFalse(plan.within_active_hours(at(22, 0), a))
        self.assertFalse(plan.within_active_hours(at(8, 59), a))

    def test_times_are_inside_hours_ordered_and_gapped(self):
        for seed in range(200):
            rng = random.Random(seed)
            start = at(rng.randint(0, 23), rng.randint(0, 59))
            times = plan.schedule_times(rng.randint(0, 40), start, PACING, rng)
            previous = start
            for when in times:
                self.assertTrue(plan.within_active_hours(when, PACING["active_hours"]), (seed, when))
                self.assertGreaterEqual(when, previous)
                previous = when

    def test_gaps_follow_the_pacing_when_nothing_is_clamped(self):
        rng = random.Random(9)
        times = plan.schedule_times(20, at(10, 0), PACING, rng)
        gaps = [(b - a).total_seconds() for a, b in zip([at(10, 0)] + times, times)]
        self.assertTrue(all(PACING["min_gap_s"] <= g <= PACING["max_gap_s"] for g in gaps), gaps)

    def test_an_action_after_closing_waits_for_the_next_morning(self):
        times = plan.schedule_times(1, at(21, 59, day=25), dict(PACING, min_gap_s=600, max_gap_s=600), random.Random(1))
        self.assertEqual(times[0], at(9, 0, day=26))

    def test_before_opening_waits_for_today(self):
        self.assertEqual(plan.schedule_times(1, at(6, 0), dict(PACING, min_gap_s=1, max_gap_s=1), random.Random(1))[0].date(), at(9, 0).date())

    def test_next_run_is_ahead_near_a_slot_and_wraps_to_tomorrow(self):
        run_at = ["10:30", "20:15"]
        for seed in range(300):
            rng = random.Random(seed)
            now = at(rng.randint(0, 23), rng.randint(0, 59))
            when = plan.next_run(now, run_at, 12, rng)
            self.assertGreater(when, now)
            slots = [dt.datetime.combine(now.date() + dt.timedelta(days=d), dt.time(int(s[:2]), int(s[3:])), tzinfo=TZ) for d in (0, 1) for s in run_at]
            self.assertTrue(any(abs((when - s).total_seconds()) <= 12 * 60 for s in slots), (now, when))
        self.assertEqual(plan.next_run(at(23, 0), ["10:30"], 0, random.Random(1)), at(10, 30, day=26))
        self.assertIsNone(plan.next_run(at(9), [], 5))


class LedgerTests(unittest.TestCase):
    def test_round_trip_and_a_half_written_last_line(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "ledger.jsonl")
            plan.append_ledger(path, {"action": "like", "ts": "2026-10-25T10:00:00+08:00", "live": True})
            with open(path, "a", encoding="utf-8") as f:
                f.write('{"action": "mess')
            self.assertEqual(len(plan.read_ledger(path)), 1)
            self.assertEqual(plan.read_ledger(os.path.join(d, "missing.jsonl")), [])

    def test_daily_remaining_counts_only_live_rows_of_today(self):
        caps = {"likes_per_day": 8, "messages_per_day": 5}
        rows = [{"action": "like", "ts": "2026-10-25T10:00:00", "live": True}] * 3 + [{"action": "like", "ts": "2026-10-24T10:00:00", "live": True}] * 4 + \
               [{"action": "like", "ts": "2026-10-25T10:00:00", "live": False}] * 2 + [{"action": "message", "ts": "2026-10-25T11:00:00", "live": True}] * 6 + \
               [{"action": "pass", "ts": "2026-10-25T10:00:00", "live": True}] * 9
        self.assertEqual(plan.daily_remaining(rows, "2026-10-25", caps), {"likes": 5, "messages": 0})
        self.assertEqual(plan.daily_remaining([], "2026-10-25", caps), {"likes": 8, "messages": 5})

    def test_random_worlds_never_go_below_zero_or_above_the_cap(self):
        for seed in range(100):
            rng = random.Random(seed)
            caps = {"likes_per_day": rng.randint(0, 10), "messages_per_day": rng.randint(0, 10)}
            rows = [{"action": rng.choice(["like", "message", "pass", "reply"]), "ts": "2026-10-%02dT10:00:00" % rng.choice([24, 25]), "live": rng.random() < 0.8} for _ in range(rng.randint(0, 40))]
            left = plan.daily_remaining(rows, "2026-10-25", caps)
            self.assertTrue(0 <= left["likes"] <= caps["likes_per_day"] and 0 <= left["messages"] <= caps["messages_per_day"], (seed, left))


if __name__ == "__main__":
    unittest.main()
