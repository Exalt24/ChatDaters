"""The decisions of the ChatDaters automation lab, as pure functions: no browser, no network, no clock of their own.

Everything the driver does is chosen here first (who to like, which opener to send, when to act, how much is left today), so each rule can be tested
without a phone and a run can be read as a plan before anything touches the app. The driver (driver.py) only carries the plan out.

Config, ledger and rules in one place:
  * config:  automation.config.json (filters, message templates, pacing, daily caps, run times), checked by validate_config.
  * ledger:  one JSON line per action in ledger.jsonl, so the daily caps survive a restart and the report has something to read.
  * rules:   decide_profile (filters with a reason), choose_template (rotation, no repeat), schedule_times and next_run (jitter inside active hours),
             daily_remaining (caps from the ledger).
"""
import datetime as dt
import json
import random
import re

PLACEHOLDER = re.compile(r"\{([a-z_]+)\}")
KNOWN_FIELDS = ("name", "first_name", "city", "region", "country", "age")
REASONS = ("ok", "age_below", "age_above", "gender", "bio_missing", "bio_blocked_word", "already_seen", "no_age", "daily_cap")
CAP = 20000   # a ledger or config is small; a larger one is refused rather than read whole


def _hm(text):
    """'09:30' -> minutes since midnight, or None when it is not a time."""
    m = re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", str(text).strip())
    return int(m.group(1)) * 60 + int(m.group(2)) if m else None


def validate_config(cfg):
    """A list of plain sentences, one per problem; an empty list means the config can be run."""
    out = []
    if not isinstance(cfg, dict):
        return ["the config must be a JSON object"]
    app = cfg.get("app") or {}
    if not str(app.get("base_url", "")).startswith(("http://", "https://")):
        out.append("app.base_url must start with http:// or https://")
    if not app.get("allowed_hosts"):
        out.append("app.allowed_hosts must list the hosts this tool may drive (the lab uses 10.0.2.2, localhost and 127.0.0.1)")
    f = cfg.get("filters") or {}
    lo, hi = f.get("min_age"), f.get("max_age")
    if not isinstance(lo, int) or not isinstance(hi, int) or lo < 18 or hi < lo:
        out.append("filters.min_age and filters.max_age must be whole numbers, min_age at least 18 and max_age not below it")
    if f.get("genders") is not None and not (isinstance(f["genders"], list) and f["genders"]):
        out.append("filters.genders must be a non-empty list or left out")
    temps = cfg.get("templates") or []
    if not temps:
        out.append("templates must hold at least one message")
    ids = set()
    for t in temps:
        tid, text = (t or {}).get("id"), (t or {}).get("text")
        if not tid or not text:
            out.append("every template needs an id and a text")
            continue
        if tid in ids:
            out.append("template id %r is used twice" % tid)
        ids.add(tid)
        for field in PLACEHOLDER.findall(text):
            if field not in KNOWN_FIELDS:
                out.append("template %r uses {%s}, which the profile does not have (known: %s)" % (tid, field, ", ".join(KNOWN_FIELDS)))
    p = cfg.get("pacing") or {}
    if not (isinstance(p.get("min_gap_s"), (int, float)) and isinstance(p.get("max_gap_s"), (int, float)) and 0 < p["min_gap_s"] <= p["max_gap_s"]):
        out.append("pacing.min_gap_s and pacing.max_gap_s must be positive and min not above max")
    ah = p.get("active_hours") or {}
    s, e = _hm(ah.get("start", "")), _hm(ah.get("end", ""))
    if s is None or e is None or s >= e:
        out.append("pacing.active_hours needs start and end as HH:MM with start before end")
    c = cfg.get("caps") or {}
    for key in ("likes_per_day", "messages_per_day"):
        if not isinstance(c.get(key), int) or c[key] < 0:
            out.append("caps.%s must be a whole number, 0 or more" % key)
    for r in (cfg.get("schedule") or {}).get("run_at", []):
        if _hm(r) is None:
            out.append("schedule.run_at has %r, which is not HH:MM" % (r,))
    return out


def load_config(path):
    with open(path, encoding="utf-8") as f:
        text = f.read(CAP + 1)
    if len(text) > CAP:
        raise ValueError("the config file is over %d characters" % CAP)
    cfg = json.loads(text)
    problems = validate_config(cfg)
    if problems:
        raise ValueError("config problems:\n  - " + "\n  - ".join(problems))
    return cfg


def host_allowed(url, allowed_hosts):
    """True only for a host on the list: the tool refuses to drive anything that is not the lab's own app."""
    m = re.match(r"^https?://([^/:?#]+)", str(url))
    return bool(m) and m.group(1).lower() in {h.lower() for h in allowed_hosts}


def parse_profile(raw):
    """A deck card as the driver reads it: name text like 'Dean Smith (34)', bio, a 'City, Region, Country' line, a gender icon class. Missing parts stay None."""
    name_text = (raw.get("name_text") or "").strip()
    m = re.match(r"^(.*?)\s*\((\d{1,3})\)\s*$", name_text)
    name, age = (m.group(1).strip(), int(m.group(2))) if m else (name_text, None)
    parts = [p.strip() for p in (raw.get("location") or "").split(",")]
    parts += [""] * (3 - len(parts))
    icon = raw.get("gender_icon") or ""
    gender = "Male" if "mars" in icon else "Female" if "venus" in icon else None
    return {"name": name, "first_name": name.split(" ")[0] if name else "", "age": age, "bio": (raw.get("bio") or "").strip(),
            "city": parts[0], "region": parts[1], "country": ", ".join(parts[2:]).strip(", "), "gender": gender}


def decide_profile(profile, filters, seen=()):
    """(like?, reason). The first rule that fails names the reason, so a report can say why a card was passed."""
    if profile["name"] in set(seen):
        return False, "already_seen"
    age = profile.get("age")
    if age is None:
        return False, "no_age"
    if age < filters["min_age"]:
        return False, "age_below"
    if age > filters["max_age"]:
        return False, "age_above"
    genders = filters.get("genders")
    if genders and profile.get("gender") not in genders:
        return False, "gender"
    bio = profile.get("bio") or ""
    if len(bio) < int(filters.get("min_bio_chars", 0)):
        return False, "bio_missing"
    low = bio.lower()
    if any(w.lower() in low for w in filters.get("blocked_bio_words", [])):
        return False, "bio_blocked_word"
    return True, "ok"


def render_template(text, profile):
    """Fill {name}, {city} and the rest; a field the profile lacks is an error, so a message never goes out with a hole in it."""
    def fill(m):
        value = profile.get(m.group(1))
        if value in (None, ""):
            raise ValueError("template needs {%s} but the profile has none" % m.group(1))
        return str(value)
    return PLACEHOLDER.sub(fill, text)


def choose_template(templates, history, profile, rng=None):
    """(template id, rendered text): the least used template first, never the same one twice in a row, ties broken by the rng so two runs differ.
    A template that cannot be filled for this profile is skipped; None when none can be."""
    rng = rng or random.Random()
    counts = {t["id"]: 0 for t in templates}
    for tid in history:
        if tid in counts:
            counts[tid] += 1
    last = history[-1] if history else None
    usable = []
    for t in templates:
        try:
            usable.append((t["id"], render_template(t["text"], profile)))
        except ValueError:
            continue
    pool = [u for u in usable if u[0] != last] or usable
    if not pool:
        return None
    fewest = min(counts[tid] for tid, _ in pool)
    return rng.choice([u for u in pool if counts[u[0]] == fewest])


def within_active_hours(when, active):
    s, e = _hm(active["start"]), _hm(active["end"])
    minute = when.hour * 60 + when.minute
    return s <= minute < e


def _clamp_into_hours(when, active):
    """A moment outside the active hours moves to the next opening: later today before the start, tomorrow's start after the end."""
    s, e = _hm(active["start"]), _hm(active["end"])
    minute = when.hour * 60 + when.minute
    if s <= minute < e:
        return when
    day = when.date() if minute < s else when.date() + dt.timedelta(days=1)
    return dt.datetime.combine(day, dt.time(s // 60, s % 60), tzinfo=when.tzinfo)


def schedule_times(count, start, pacing, rng=None):
    """The moments for `count` actions: random gaps between min_gap_s and max_gap_s, every moment inside the active hours (an action that would land outside waits for the next opening)."""
    rng = rng or random.Random()
    out, now = [], _clamp_into_hours(start, pacing["active_hours"])
    for _ in range(count):
        now = _clamp_into_hours(now + dt.timedelta(seconds=rng.uniform(pacing["min_gap_s"], pacing["max_gap_s"])), pacing["active_hours"])
        out.append(now)
    return out


def next_run(now, run_at, jitter_minutes, rng=None):
    """The next scheduled run after `now`: the earliest run_at time still ahead (tomorrow's first one when today's are past), shifted by up to jitter_minutes either way but never before `now`."""
    rng = rng or random.Random()
    if not run_at:
        return None
    slots = sorted(_hm(r) for r in run_at)
    for day_offset in (0, 1):
        for minutes in slots:
            base = dt.datetime.combine(now.date() + dt.timedelta(days=day_offset), dt.time(minutes // 60, minutes % 60), tzinfo=now.tzinfo)
            if base > now:
                shifted = base + dt.timedelta(minutes=rng.uniform(-jitter_minutes, jitter_minutes))
                return shifted if shifted > now else base
    return None


def read_ledger(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f.read(CAP * 50).splitlines():
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue   # a half-written last line must not stop the next run
    except FileNotFoundError:
        pass
    return rows


def append_ledger(path, row):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def daily_remaining(rows, today, caps):
    """What is left of today's caps, counted from the ledger's own 'like' and 'message' rows dated today (YYYY-MM-DD in each row's ts)."""
    day = str(today)
    used = {"like": 0, "message": 0}
    for r in rows:
        if r.get("action") in used and str(r.get("ts", ""))[:10] == day and r.get("live"):
            used[r["action"]] += 1
    return {"likes": max(0, caps["likes_per_day"] - used["like"]), "messages": max(0, caps["messages_per_day"] - used["message"])}
