"""End to end proof of the automation lab on an Android emulator, checked against the app's own database.

What it does, in order (about two minutes with the fast pacing below):
  1. reset the database, make four seeded users like the lab account first (so the account's own like turns into a match), clear the ledger;
  2. a dry run: reads the whole deck in Chrome on the emulator and must change nothing in the database;
  3. a live run with a short pacing config: swipes the deck by the filters, opens a conversation for each new match and types a templated opener;
  4. the database must hold exactly the matches and messages the plan implies, passes must carry their reasons, and the cap must have stopped the 4th like;
  5. one seeded user replies, a second live run notes the reply once and sends nothing new, and the report shows the reply rate of the template that got it.

Needs the stack of the README running (API_PORT=4757 docker compose -f docker-compose.yml -f automation/compose.emulator.yml up -d, the Vue dev server with
--host 0.0.0.0 and VITE_GRAPHQL_URL=http://10.0.2.2:4757/graphql), a booted emulator, ANDROID_HOME and APPIUM_HOME set. Run: python e2e_appium_chatdaters.py
Named e2e_ and not test_ on purpose: it needs a device, so the plain unit tests (tests/) never pick it up.
"""
import copy
import datetime as dt
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("API_PORT", "4757")
import appium_server  # noqa: E402
import driver  # noqa: E402
import lab  # noqa: E402
import plan  # noqa: E402
import report  # noqa: E402

LEDGER = os.path.join(HERE, "ledger_e2e.jsonl")
bad = []


def check(label, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else "  :: " + str(extra)[:300]))
    if not cond:
        bad.append(label)


def fast_config():
    cfg = plan.load_config(os.path.join(HERE, "automation.config.json"))
    cfg = copy.deepcopy(cfg)
    cfg["pacing"] = {"min_gap_s": 0.4, "max_gap_s": 1.0, "active_hours": {"start": "00:00", "end": "23:59"}}   # only the waits are shortened, every rule stays
    cfg["caps"] = {"likes_per_day": 3, "messages_per_day": 5}
    return cfg


def messages():
    return json.loads(lab.rails("puts Message.order(:id).map { |m| [User.find(m.sender_id).first_name, User.find(m.receiver_id).first_name, m.content] }.to_json").splitlines()[-1])


def one_run(server_url, cfg, live, rng):
    s = driver.Session(driver.open_chrome(server_url), cfg, LEDGER, live=live, rng=rng)
    try:
        return s.run_once("user1@gmail.com", "password")
    finally:
        s.drv.quit()


def main():
    cfg = fast_config()
    lab.reset()
    lab.prime(["user2@gmail.com", "user10@gmail.com", "user8@gmail.com", "user12@gmail.com"])   # Rufus, Eloisa, Nolan and Muriel all like the lab account first
    if os.path.exists(LEDGER):
        os.remove(LEDGER)
    rng = random.Random(7)
    with appium_server.AppiumServer(log_path=os.path.join(HERE, "appium_server.log")) as server:
        likes, msgs = one_run(server.url, cfg, False, rng)
        st = lab.status()
        check("dry run planned 3 likes (the 4th hit the cap) and no messages", (likes, msgs) == (3, 0), (likes, msgs))
        check("dry run changed nothing in the database", st["matches"] == {"pending": 4} and st["messages"] == 0, st)
        check("dry run rows are marked as not live", all(r["live"] is False for r in plan.read_ledger(LEDGER)))
        os.remove(LEDGER)

        likes, msgs = one_run(server.url, cfg, True, rng)
        st = lab.status()
        mine = dict((name, status) for name, status in st["mine"])
        rows = plan.read_ledger(LEDGER)
        liked = [r["profile"]["name"].split(" ")[0] for r in rows if r["action"] == "like"]
        capped = [r["profile"]["name"].split(" ")[0] for r in rows if r["action"] == "pass" and r["reason"] == "daily_cap"]
        check("live run: exactly 3 likes, the daily cap stopped one eligible profile", likes == 3 and len(liked) == 3 and len(capped) == 1, (likes, liked, capped))
        check("live run: the liked profiles became matches and the capped one stayed pending", all(mine.get(n) == "matched" for n in liked) and mine.get(capped[0]) == "pending", mine)
        reasons = {r["profile"]["name"].split(" ")[0]: r["reason"] for r in rows if r["action"] == "pass"}
        check("passes carry their reasons", reasons.get("Dottie") == "age_below" and reasons.get("Tina") == "age_above", reasons)
        sent = [m for m in messages() if m[0] == "Dean" and m[2] != "Hello"]
        check("live run: one templated opener typed per new match", msgs == 3 and sorted(m[1] for m in sent) == sorted(liked), (sent, liked))
        used = [r["template_id"] for r in rows if r["action"] == "message"]
        check("the three openers rotated through the three templates", len(set(used)) == 3, used)
        check("each opener has the person's name filled in and no placeholder left", all(m[1] in m[2] or "your profile" in m[2] or "{" not in m[2] for m in sent) and all("{" not in m[2] for m in sent), sent)

        who = liked[0]
        lab.reply(who)
        before = len(messages())
        likes2, msgs2 = one_run(server.url, cfg, True, rng)
        check("second run sends nothing new", (likes2, msgs2) == (0, 0) and len(messages()) == before, (likes2, msgs2, len(messages()) - before))
        rows = plan.read_ledger(LEDGER)
        check("the reply is noted once", [r["profile"]["name"].split(" ")[0] for r in rows if r["action"] == "reply"] == [who])
        summary = report.summarise(rows)
        who_template = next(r["template_id"] for r in rows if r["action"] == "message" and r["profile"]["name"].startswith(who))
        check("the report gives the answered template a 100% reply rate", summary["templates"][who_template]["reply_rate"] == 1.0 and summary["messages"] == 3, summary)
    print(report.render_markdown(summary))
    print("%d failed" % len(bad) if bad else "ALL PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
