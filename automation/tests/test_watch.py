"""Unit tests for the scheduled loop in run.py (watch_loop): it waits for each run time, runs, survives a failed run, and stops on an empty schedule.
A fake clock stands in for time: every sleep moves it, so the tests take no real time."""
import datetime as dt
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import run  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=8))


class FakeClock:
    def __init__(self, start):
        self.t = start
        self.slept = 0

    def now(self):
        return self.t

    def sleep(self, seconds):
        self.slept += 1
        self.t += dt.timedelta(seconds=seconds)


class WatchTests(unittest.TestCase):
    def test_runs_start_at_each_scheduled_time_in_order(self):
        clock = FakeClock(dt.datetime(2026, 10, 25, 8, 0, tzinfo=TZ))
        starts = []
        n = run.watch_loop({"run_at": ["10:30", "20:15"], "jitter_minutes": 0}, lambda: starts.append(clock.now()), clock.now, clock.sleep, random.Random(1), max_runs=3, log=lambda *_: None)
        self.assertEqual(n, 3)
        self.assertEqual([(s.day, s.hour, s.minute) for s in starts], [(25, 10, 30), (25, 20, 15), (26, 10, 30)])

    def test_jitter_keeps_every_run_near_its_slot_and_never_early(self):
        for seed in range(50):
            clock = FakeClock(dt.datetime(2026, 10, 25, 9, 0, tzinfo=TZ))
            starts = []
            run.watch_loop({"run_at": ["10:30"], "jitter_minutes": 12}, lambda: starts.append(clock.now()), clock.now, clock.sleep, random.Random(seed), max_runs=2, log=lambda *_: None)
            for s in starts:
                slot = dt.datetime.combine(s.date(), dt.time(10, 30), tzinfo=TZ)
                self.assertLessEqual(abs((s - slot).total_seconds()), 12 * 60 + 1.0, (seed, s))
            self.assertGreater(starts[1], starts[0])

    def test_a_failed_run_does_not_end_the_schedule(self):
        clock = FakeClock(dt.datetime(2026, 10, 25, 8, 0, tzinfo=TZ))
        calls, logs = [], []

        def flaky():
            calls.append(clock.now())
            if len(calls) == 1:
                raise RuntimeError("the emulator was off")

        n = run.watch_loop({"run_at": ["10:30"], "jitter_minutes": 0}, flaky, clock.now, clock.sleep, random.Random(1), max_runs=2, log=logs.append)
        self.assertEqual((n, len(calls)), (2, 2))
        self.assertTrue(any("run failed: the emulator was off" in line for line in logs))

    def test_an_empty_schedule_stops_at_once(self):
        clock = FakeClock(dt.datetime(2026, 10, 25, 8, 0, tzinfo=TZ))
        called = []
        self.assertEqual(run.watch_loop({"run_at": []}, lambda: called.append(1), clock.now, clock.sleep, random.Random(1), max_runs=3, log=lambda *_: None), -1)
        self.assertEqual((called, clock.slept), ([], 0))

    def test_it_waits_by_sleeping_not_by_running_early(self):
        clock = FakeClock(dt.datetime(2026, 10, 25, 10, 29, tzinfo=TZ))
        starts = []
        run.watch_loop({"run_at": ["10:30"], "jitter_minutes": 0}, lambda: starts.append(clock.now()), clock.now, clock.sleep, random.Random(1), max_runs=1, log=lambda *_: None)
        self.assertGreaterEqual(starts[0], dt.datetime(2026, 10, 25, 10, 30, tzinfo=TZ))
        self.assertGreater(clock.slept, 0)


if __name__ == "__main__":
    unittest.main()
