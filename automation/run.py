"""Command line for the ChatDaters automation lab.

  python run.py check                 validate automation.config.json and print the pacing and caps it sets
  python run.py plan                  dry run: log in, read the whole deck, print who would be liked or passed and why; changes nothing
  python run.py run --live            carry the plan out: swipes, first messages, reply notes, paced like the config says
  python run.py watch --live          repeat run at the config's schedule.run_at times, with jitter, until stopped
  python run.py report                read ledger.jsonl and print the report

Dry run is the default. --live is needed to change anything, and the tool refuses any host that is not on app.allowed_hosts.
The account is read from CHATDATERS_EMAIL and CHATDATERS_PASSWORD (the seeded lab account user1@gmail.com / password when unset).
"""
import argparse
import datetime as dt
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan  # noqa: E402
import report  # noqa: E402

LEDGER = os.path.join(HERE, "ledger.jsonl")
DEFAULT_CONFIG = os.path.join(HERE, "automation.config.json")


def account():
    return os.environ.get("CHATDATERS_EMAIL", "user1@gmail.com"), os.environ.get("CHATDATERS_PASSWORD", "password")


def cmd_check(cfg):
    print("config ok")
    print("pacing: %s to %s seconds between actions, active %s to %s" % (cfg["pacing"]["min_gap_s"], cfg["pacing"]["max_gap_s"],
                                                                         cfg["pacing"]["active_hours"]["start"], cfg["pacing"]["active_hours"]["end"]))
    print("caps per day: %d likes, %d messages" % (cfg["caps"]["likes_per_day"], cfg["caps"]["messages_per_day"]))
    print("runs at: %s (+/- %s minutes)" % (", ".join(cfg.get("schedule", {}).get("run_at", [])) or "not scheduled", cfg.get("schedule", {}).get("jitter_minutes", 0)))
    return 0


def session(cfg, live, server_url):
    import driver
    return driver.Session(driver.open_chrome(server_url), cfg, LEDGER, live=live)


def with_server(args, fn):
    """Use the Appium server at --appium-url when one answers, else start one for this run and stop it after."""
    import appium_server
    if args.appium_url:
        return fn(args.appium_url)
    with appium_server.AppiumServer(log_path=os.path.join(HERE, "appium_server.log")) as server:
        return fn(server.url)


def cmd_run(cfg, args, live):
    email, password = account()

    def go(url):
        s = session(cfg, live, url)
        try:
            likes, messages = s.run_once(email, password)
        finally:
            s.drv.quit()
        print("%s: %d likes, %d first messages" % ("done" if live else "planned (nothing changed)", likes, messages))
    with_server(args, go)
    return 0


def watch_loop(sched, run, now, sleep, rng, max_runs=None, log=print):
    """Wait for each scheduled time (run_at with jitter), call run(), repeat. The clock, the sleep, the run and the random source are passed in so the loop is testable
    without waiting; a failed run is logged and the schedule goes on. Returns the number of runs started, or -1 when the schedule is empty."""
    started = 0
    while max_runs is None or started < max_runs:
        when = plan.next_run(now(), sched.get("run_at", []), sched.get("jitter_minutes", 0), rng)
        if when is None:
            log("schedule.run_at is empty: nothing to wait for")
            return -1
        log("next run at %s" % when.isoformat(timespec="minutes"))
        while now() < when:
            sleep(1.0)
        started += 1
        try:
            run()
        except Exception as exc:  # noqa: BLE001  one failed run must not end the schedule
            log("run failed: %s" % exc)
    return started


def cmd_watch(cfg, args):
    status = watch_loop(cfg.get("schedule", {}), lambda: cmd_run(cfg, args, True), lambda: dt.datetime.now().astimezone(), time.sleep, random.Random(), max_runs=args.max_runs)
    return 1 if status < 0 else 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("check", "plan", "run", "watch", "report"))
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--live", action="store_true", help="change things in the app (without it every command is read-only)")
    ap.add_argument("--appium-url", default="", help="use a server that is already running instead of starting one")
    ap.add_argument("--max-runs", type=int, default=None, help="watch only: stop after this many runs (default: keep going until stopped)")
    args = ap.parse_args(argv)
    if args.command in ("run", "watch") and not args.live:
        print("run and watch change things: add --live, or use `plan` for a read-only look")
        return 2
    try:
        cfg = plan.load_config(args.config)
    except (OSError, ValueError) as exc:
        print(exc)
        return 2
    if args.command == "check":
        return cmd_check(cfg)
    if args.command == "report":
        print(report.render_markdown(report.summarise(plan.read_ledger(LEDGER))))
        return 0
    if args.command == "plan":
        return cmd_run(cfg, args, False)
    if args.command == "watch":
        return cmd_watch(cfg, args)
    return cmd_run(cfg, args, True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
