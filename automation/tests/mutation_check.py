# LIFESPAN: permanent
"""Proof that the tests can fail: break plan.py or report.py in one small way at a time, in a temporary copy, and require the unit tests to turn red.

A mutant whose target text is gone fails the run loudly (the file was reworded and the check went stale), and a mutant the tests do not catch fails it too.
Run from the repo root: python automation/tests/mutation_check.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUTOMATION = os.path.dirname(HERE)

MUTANTS = [
    ("plan.py", "a profile at the minimum age is passed", 'age < filters["min_age"]', 'age <= filters["min_age"]'),
    ("plan.py", "a profile at the maximum age is passed", 'age > filters["max_age"]', 'age >= filters["max_age"]'),
    ("plan.py", "a seen profile is liked again", 'if profile["name"] in set(seen):', "if False:"),
    ("plan.py", "the gender filter is ignored", 'if genders and profile.get("gender") not in genders:', "if False:"),
    ("plan.py", "a bio exactly at the minimum is rejected", 'if len(bio) < int(filters.get("min_bio_chars", 0)):', 'if len(bio) <= int(filters.get("min_bio_chars", 0)):'),
    ("plan.py", "blocked words are ignored", "if any(w.lower() in low for w in filters.get(\"blocked_bio_words\", [])):", "if False:"),
    ("plan.py", "the same template may repeat", "pool = [u for u in usable if u[0] != last] or usable", "pool = usable"),
    ("plan.py", "the most used template is chosen", "fewest = min(counts[tid] for tid, _ in pool)", "fewest = max(counts[tid] for tid, _ in pool)"),
    ("plan.py", "a message goes out with a hole in it", 'if value in (None, ""):', "if False:"),
    ("plan.py", "actions are not kept inside the active hours", "now = _clamp_into_hours(now + dt.timedelta(seconds=rng.uniform(pacing[\"min_gap_s\"], pacing[\"max_gap_s\"])), pacing[\"active_hours\"])",
     "now = now + dt.timedelta(seconds=rng.uniform(pacing[\"min_gap_s\"], pacing[\"max_gap_s\"]))"),
    ("plan.py", "the next run may be in the past", "if base > now:", "if True:"),
    ("plan.py", "dry-run rows count against the daily cap", 'and r.get("live"):', ":"),
    ("plan.py", "yesterday's rows count against today's cap", 'and str(r.get("ts", ""))[:10] == day', ""),
    ("plan.py", "any host that mentions an allowed name passes", "m.group(1).lower() in {h.lower() for h in allowed_hosts}", "any(h.lower() in str(url).lower() for h in allowed_hosts)"),
    ("plan.py", "a minor can be configured", "lo < 18", "lo < 0"),
    ("plan.py", "a template with an unknown field validates", "if field not in KNOWN_FIELDS:", "if False:"),
    ("run.py", "the watch loop runs before its time", "while now() < when:", "while False:"),
    ("run.py", "one failed run ends the schedule", "except Exception as exc:  # noqa: BLE001  one failed run", "except KeyboardInterrupt as exc:  # noqa: BLE001  one failed run"),
    ("run.py", "an empty schedule loops forever", "return -1", "continue"),
    ("report.py", "one conversation counts as many answers", "if key not in answered and r.get(\"template_id\") in per_template:", "if r.get(\"template_id\") in per_template:"),
    ("report.py", "dry-run rows count as live likes", 'live = [r for r in rows if r.get("live")]', "live = list(rows)"),
]


def run_tests(cwd):
    """The unit tests' exit code. A mutant that makes the code loop forever hangs the tests, and a hang is as red as a failure (the suite takes about 2 s, so 30 s is generous)."""
    try:
        return subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30).returncode
    except subprocess.TimeoutExpired:
        return 1


def main():
    bad = 0
    for filename, label, old, new in MUTANTS:
        with tempfile.TemporaryDirectory() as tmp:
            work = os.path.join(tmp, "automation")
            shutil.copytree(AUTOMATION, work, ignore=shutil.ignore_patterns("__pycache__", "*.jsonl", "*.log"))
            target = os.path.join(work, filename)
            with open(target, encoding="utf-8") as f:
                src = f.read()
            if old not in src:
                print("STALE    %s (the target text is gone from %s)" % (label, filename))
                bad += 1
                continue
            with open(target, "w", encoding="utf-8") as f:
                f.write(src.replace(old, new, 1))
            red = run_tests(work) != 0
            print("%-8s %s" % ("CAUGHT" if red else "SURVIVED", label))
            bad += 0 if red else 1
    green = run_tests(AUTOMATION) == 0
    print("the untouched code is %s" % ("green" if green else "RED"))
    return 0 if green and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
