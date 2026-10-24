# Automation lab

A small tool that drives the ChatDaters web app in Chrome on an Android emulator through Appium. It swipes the deck by filters from one config file, sends a templated first message to each new match, paces itself, stops at daily caps, and writes a report. It exists to test and show mobile app automation on an app I own, with seeded demo accounts. It is not meant for any other app.

## What is in the folder

| File | What it does |
|---|---|
| `automation/automation.config.json` | Filters, message templates, pacing, daily caps and run times. The only file a user edits. |
| `automation/plan.py` | The decisions, as pure functions: config check, who to like or pass and why, which template to send, when to act, what is left of today's caps. |
| `automation/driver.py` | Reads the page, clicks, types and waits. Carries out what `plan.py` decided and never acts on a host that is not on the allowed list. |
| `automation/report.py` | Reads the ledger and prints likes, passes with reasons, messages and the reply rate of each template. |
| `automation/run.py` | The command line: `check`, `plan`, `run --live`, `watch --live`, `report`. |
| `automation/lab.py` | Puts the seeded database in a known state and reads it back, for the end to end test. |
| `automation/appium_server.py` | Starts an Appium server as a child of the run and stops it again. |
| `automation/e2e_appium_chatdaters.py` | The end to end proof on the emulator, checked against the database. |
| `automation/tests/` | Unit tests for `plan.py` and `report.py`, and a mutation check that breaks them on purpose. |

## Run it

You need the stack from the main README running with the emulator override, a booted Android emulator (or a phone with USB debugging), `ANDROID_HOME` set, and Appium with its UiAutomator2 driver (`npm install -g appium`, then `appium driver install uiautomator2`, then `pip install Appium-Python-Client`).

```bash
API_PORT=4757 docker compose -f docker-compose.yml -f automation/compose.emulator.yml up --build -d
API_PORT=4757 docker compose -f docker-compose.yml -f automation/compose.emulator.yml exec api bin/rails db:seed
cd frontend && npm install && VITE_GRAPHQL_URL=http://10.0.2.2:4757/graphql npm run dev -- --host 0.0.0.0
cd automation && python run.py check
python run.py plan
```

`10.0.2.2` is how the Android emulator reaches the PC. The override file `compose.emulator.yml` makes the API hand out image URLs on that address. `run.py check` validates the config. `run.py plan` is a dry run: it logs in as `user1@gmail.com`, reads the whole deck and prints who would be liked or passed and why, and changes nothing. `run.py run --live` carries the plan out.

## The config

```json
"filters":  { "min_age": 25, "max_age": 45, "genders": ["Male"], "min_bio_chars": 10, "blocked_bio_words": ["crypto", "onlyfans"] },
"templates": [ { "id": "short-hello", "text": "Hi {first_name}, your profile caught my eye. How is your week going?" } ],
"pacing":   { "min_gap_s": 20, "max_gap_s": 90, "active_hours": { "start": "09:00", "end": "22:00" } },
"caps":     { "likes_per_day": 8, "messages_per_day": 5 },
"schedule": { "run_at": ["10:30", "20:15"], "jitter_minutes": 12 }
```

A template may use `{name}`, `{first_name}`, `{city}`, `{region}`, `{country}` and `{age}`. The config check names every problem in plain words (a template using a field the profile does not have, a minimum age under 18, hours that run backwards). A template that cannot be filled for a profile is skipped, so a message never goes out with a hole in it. Templates are used least first and never the same one twice in a row.

## Safety defaults

- Every command is read only unless `--live` is given.
- The tool refuses to run when `app.base_url` is not on `app.allowed_hosts` (the lab allows `10.0.2.2`, `localhost` and `127.0.0.1`).
- A live run outside the active hours does not start.
- The daily caps are counted from the ledger, so they hold across restarts. The defaults are small: eight likes a day is the free number Hinge states on its mission page.
- It uses one account, the seeded one. It never creates accounts and never messages anyone who did not match with it.

## How it was checked

- **Unit tests:** `python -m unittest discover -s automation/tests -v` runs 33 tests on the pure rules: a table for each filter and config rule, and seeded random worlds for the rules that carry state (template rotation stays balanced over 60 sends, every scheduled time sits inside the active hours, the next run is always ahead of now, the caps never go below zero).
- **Mutation check:** `python automation/tests/mutation_check.py` breaks `plan.py` or `report.py` in 18 small ways, one at a time, in a temporary copy (a boundary moved by one, a filter switched off, dry run rows counted as live) and requires the tests to turn red each time. All 18 are caught. The first version missed one (a bio exactly at the minimum length); a boundary test was added.
- **End to end on the emulator:** `python automation/e2e_appium_chatdaters.py` resets the database, makes four seeded users like the lab account first, runs a dry run, a live run and a second live run in Chrome on the emulator, and checks 12 things against the real records: the dry run changed nothing, three likes and one stopped by the cap, the liked profiles became matches, each pass has its reason, one opener per new match using three different templates, nothing new on the second run, one reply noted once, and the reply rate of the template that got it. After the app fix it passed on seven of eight runs on 2026-10-25 (the one failure is the second item under What broke).

## What broke

The first live run failed on the first message of a new conversation. The page logged `Error starting conversation: Cannot access 'data' before initialization`, and the matches page never opened the chat. The cause was in `frontend/src/views/User/Matches.vue`: the cache update inside `createFirstMessage` read `data.currentUser.id` from the value the same call was still producing. That branch runs only when the Apollo cache holds no conversation list in the shape the update asks for. The live run reloads the matches page before every chat, and it failed on that step in three runs in a row; two single clicks in a debug session opened the chat without the error, so what the cache holds decides it. The fix reads the id from `this.currentUser.id`. The same run on the fixed code passes.

The second thing that broke was the driver. Once it started closing Chrome's "Change your password" sheet (the seeded password is on Chrome's breach list), the timing shifted and one run read a conversation before its thread had loaded, so it missed a reply and counted the load as a new message. The driver now waits until the thread lists a message before it reads or types, and the next two runs passed.

## What the apps say about automation

I read the terms and help pages of the apps this kind of tool gets pointed at on 2026-10-25. They ban it:

- Hinge: "Using third-party tools like autoswipers, bots, scrapers, or any kind of automation software on Hinge is a violation of our Terms of Use."
- Tinder's terms bar anyone from using "any robot, crawler, site search/retrieval application, proxy or other manual or automatic device, method or process to access, retrieve, index, "data mine,"..."
- Bumble: "we don't allow unauthorized automated behaviors that undermine or interfere with our platform. These behaviors can include scraping, scripting, or artificially influencing connections or interactions..."
- Instagram's terms bar "accessing or collecting information in an automated way without our express permission, regardless of whether such automated access or collection is undertaken while logged-in to an Instagram account."

That is why this lab runs against its own app and seeded accounts only. Pacing is also not a guarantee of anything on a real service. The instagrapi maintainers write that "Instagram risk checks depend on the full account/session/IP/action pattern: account age and trust, device consistency, proxy reputation, request volume, action mix, repeated fresh logins, prior challenges, and server-side experiments", and users there report being flagged with random gaps between actions and with read only use. The apps also say they use more than timing: Google's Play Integrity documentation lists emulated environments, hyperactive devices and other apps that can control input among the signals an app can ask for. Where an official route exists it is the one to use: Meta's Instagram platform allows scheduled publishing and automated replies for professional accounts through an approved app, with published limits.

## Limits

- It drives one app, in Chrome, on an emulator. It does not read or control a native Android or iOS app. iOS needs a macOS host or a real iPhone, and neither is part of this lab.
- The deck order changes on every page load, so a run cannot be replayed in the same order. The tests assert what must hold in any order.
- Profiles are matched by name, so two profiles with the same name look like one.
- The app opens every new conversation with a fixed "Hello" before the tool types its own first message.
- The end to end test needs a device, so it does not run in CI. CI runs the unit tests and the mutation check.
