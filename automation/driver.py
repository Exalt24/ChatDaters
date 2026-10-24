"""Carries a plan out in Chrome on an Android device or emulator, through Appium (UiAutomator2 + chromedriver).

Every decision comes from plan.py. This file only reads the page, clicks, types and waits, and it never acts on a host that is not on the config's
allowed list. A dry run (live=False) reads the whole deck from the page and changes nothing: no like, no pass, no message.

Waiting is always a short poll that reads the page (poll), never one long sleep, so a slow load or a missing button shows up in seconds.
"""
import datetime as dt
import random
import time

import plan

POLL_S = 0.25
TYPE_CHUNK = (2, 5)          # characters per keystroke burst while typing a message
TYPE_PAUSE_S = (0.04, 0.16)  # pause between bursts
JS_CARDS = """
return Array.from(document.querySelectorAll('.swipe-container .card')).map(function (c) {
  var strong = c.querySelector('strong'), bio = c.querySelector('.bio'), icon = c.querySelector('i.gender-icon');
  var marker = c.querySelector('i.pi-map-marker'), where = marker && marker.parentElement ? marker.parentElement.innerText : '';
  return {name_text: strong ? strong.innerText.replace(/\\s+/g, ' ') : '', bio: bio ? bio.innerText : '', gender_icon: icon ? icon.className : '', location: where};
});
"""
JS_CLICK = "var el = document.querySelector(arguments[0]); if (!el) return false; el.click(); return true;"


class DriverError(RuntimeError):
    pass


def poll(fn, timeout=8.0, step=POLL_S, what="the page"):
    """Call fn every step until it returns something truthy; raise with what was awaited when the time is up."""
    deadline = time.monotonic() + timeout
    while True:
        value = fn()
        if value:
            return value
        if time.monotonic() >= deadline:
            raise DriverError("timed out after %.0f s waiting for %s" % (timeout, what))
        time.sleep(step)


def open_chrome(server_url):
    """One Chrome session on the connected device; the caller quits it."""
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.browser_name = "Chrome"
    opts.set_capability("appium:chromedriverAutodownload", True)
    opts.set_capability("appium:chromeOptions", {"args": ["--no-first-run", "--disable-fre", "--no-default-browser-check"]})
    opts.new_command_timeout = 300
    drv = webdriver.Remote(server_url, options=opts)
    drv.implicitly_wait(0)
    return drv


class Session:
    def __init__(self, drv, cfg, ledger_path, live=False, rng=None, clock=None):
        base = cfg["app"]["base_url"].rstrip("/")
        if not plan.host_allowed(base, cfg["app"]["allowed_hosts"]):
            raise DriverError("%s is not on app.allowed_hosts: this tool only drives the app it was set up for" % base)
        self.drv, self.cfg, self.ledger_path, self.live = drv, cfg, ledger_path, live
        self.base = base
        self.rng = rng or random.Random()
        self.clock = clock or (lambda: dt.datetime.now().astimezone())
        self.user_id = None

    # ---- ledger ----
    def record(self, action, profile=None, reason="", template_id=None, text=None):
        plan.append_ledger(self.ledger_path, {"ts": self.clock().isoformat(timespec="seconds"), "action": action, "live": self.live, "profile": profile or {},
                                              "reason": reason, "template_id": template_id, "text": text})

    # ---- page helpers ----
    def go(self, path):
        self.drv.get(self.base + path)

    def js(self, script, *args):
        return self.drv.execute_script(script, *args)

    def click(self, selector, timeout=8.0):
        poll(lambda: self.js(JS_CLICK, selector), timeout, what="a click on " + selector)

    def pace(self, seconds):
        """Wait like a person would between actions, but keep reading the page every tick so a crash or a logout is seen at once."""
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            self.js("return document.readyState")
            time.sleep(min(POLL_S, max(0.0, deadline - time.monotonic())))

    def gap(self):
        p = self.cfg["pacing"]
        self.pace(self.rng.uniform(p["min_gap_s"], p["max_gap_s"]))

    # ---- app steps ----
    def login(self, email, password):
        from selenium.webdriver.common.by import By
        self.go("/login")
        poll(lambda: self.drv.find_elements(By.CSS_SELECTOR, "#email"), what="the login form")
        self.drv.find_element(By.CSS_SELECTOR, "#email").send_keys(email)
        self.drv.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
        self.click(".login-button")
        self.user_id = poll(self._signed_in_id, 15, what="the signed-in header with the Swipe link")
        self.dismiss_password_sheet()
        return self.user_id

    def dismiss_password_sheet(self):
        """The seeded password ("password") is on Chrome's breach list, so Chrome puts a native "Change your password" sheet over the page after login.
        It does not stop the page, but it hides the app on screen, so it is closed through the native context when it shows (looked for for about 3 s)."""
        from selenium.webdriver.common.by import By
        web = self.drv.current_context
        try:
            self.drv.switch_to.context("NATIVE_APP")
            deadline = time.monotonic() + 3.0
            while time.monotonic() < deadline:
                found = self.drv.find_elements(By.XPATH, "//*[@text='Change your password']")
                if found:
                    self.drv.find_element(By.XPATH, "//*[@text='OK' or @content-desc='OK']").click()
                    return True
                time.sleep(POLL_S)
            return False
        except Exception:  # noqa: BLE001  a sheet that cannot be closed must not stop the run: the page still works behind it
            return False
        finally:
            self.drv.switch_to.context(web)

    def _signed_in_id(self):
        """The app lands on the home page after login, so the account's id is read from the header's Swipe link (/<id>/swipe)."""
        href = self.js("var a = Array.from(document.querySelectorAll('a')).find(function (x) { return /^\\/\\d+\\/swipe$/.test(x.getAttribute('href') || ''); }); return a ? a.getAttribute('href') : null;")
        return href.strip("/").split("/")[0] if href else None

    def deck(self):
        poll(lambda: self.js("return !!document.querySelector('.swipe-container .card') || /No more users/.test(document.body.innerText)"), 12, what="the swipe deck")
        return [plan.parse_profile(raw) for raw in self.js(JS_CARDS)]

    def swipe_top(self, like):
        before = len(self.js(JS_CARDS))
        self.click('.btns img[src="/like.png"]' if like else '.btns img[src="/nope.png"]')
        poll(lambda: len(self.js(JS_CARDS)) < before, 10, what="the top card to leave the deck")

    def match_names(self):
        self.go("/%s/matches" % self.user_id)
        poll(lambda: self.js("return !!document.querySelector('.match-card') || /No matches found/.test(document.body.innerText)"), 12, what="the matches page")
        return self.js("return Array.from(document.querySelectorAll('.match-card h3')).map(function (h) { return h.innerText.trim(); });")

    def open_conversation(self, name):
        names = self.match_names()
        if name not in names:
            raise DriverError("no match named %r on the matches page" % name)
        index = names.index(name)
        self.js("window.__errs = []; window.addEventListener('unhandledrejection', function (e) { window.__errs.push('rejected: ' + String(e.reason)); });"
                " var c = console.error; console.error = function () { window.__errs.push(Array.from(arguments).join(' ').slice(0, 200)); c.apply(console, arguments); };"
                " document.querySelectorAll('.match-card')[arguments[0]].querySelector('.message-btn').click();", index)
        try:
            poll(lambda: self.js("return !!document.querySelector('.message-input input')"), 12, what="the conversation")
        except DriverError as exc:
            seen = self.js("return document.body.innerText.replace(/\\s+/g, ' ').slice(0, 160)")
            errs = self.js("return window.__errs") or []
            raise DriverError("%s (at %s, the page says: %s, the page logged: %s)" % (exc, self.drv.current_url, seen, errs[:3])) from exc
        # The input box shows before the thread has loaded. The app opens every conversation with a message, so a thread is loaded once it lists one;
        # reading earlier would count the load itself as a new message or miss a reply.
        poll(self.messages, 10, what="the messages of the conversation")

    def messages(self):
        return self.js("return Array.from(document.querySelectorAll('.messages-list > div')).map(function (d) { var c = d.querySelector('.message-content');"
                       " return {text: c ? c.innerText : '', sent: /message-sent/.test(d.className)}; });")

    def type_and_send(self, text):
        from selenium.webdriver.common.by import By
        field = poll(lambda: self.drv.find_elements(By.CSS_SELECTOR, ".message-input input"), what="the message box")[0]
        i = 0
        while i < len(text):
            n = self.rng.randint(*TYPE_CHUNK)
            field.send_keys(text[i:i + n])
            i += n
            time.sleep(self.rng.uniform(*TYPE_PAUSE_S))
        before = len(self.messages())
        self.drv.find_element(By.CSS_SELECTOR, ".message-input button").click()
        poll(lambda: len(self.messages()) > before, 10, what="the sent message to appear")

    # ---- one run ----
    def run_once(self, email, password, now=None):
        """Login, work the deck, open conversations for new matches, note replies. Returns the number of likes and messages done (or planned in a dry run)."""
        cfg = self.cfg
        now = now or self.clock()
        if self.live and not plan.within_active_hours(now, cfg["pacing"]["active_hours"]):
            raise DriverError("outside the active hours %s: a live run waits for the next opening" % cfg["pacing"]["active_hours"])
        remaining = plan.daily_remaining(plan.read_ledger(self.ledger_path), now.date(), cfg["caps"])
        self.login(email, password)
        self.go("/%s/swipe" % self.user_id)
        done_likes = done_messages = 0
        seen = {r["profile"].get("name") for r in plan.read_ledger(self.ledger_path) if r.get("live") == self.live and r.get("action") in ("like", "pass") and r.get("profile")}
        for profile in self.deck():
            like, reason = plan.decide_profile(profile, cfg["filters"], seen)
            if like and remaining["likes"] <= 0:
                like, reason = False, "daily_cap"
            self.record("like" if like else "pass", profile, reason)
            if like:
                remaining["likes"] -= 1
                done_likes += 1
            if self.live:
                self.swipe_top(like)
                self.gap()
        if not self.live:
            return done_likes, 0
        sent_to = {r["profile"].get("name") for r in plan.read_ledger(self.ledger_path) if r.get("action") == "message" and r.get("live")}
        history = [r["template_id"] for r in plan.read_ledger(self.ledger_path) if r.get("action") == "message" and r.get("live")]
        liked = {r["profile"]["name"]: r["profile"] for r in plan.read_ledger(self.ledger_path) if r.get("action") == "like" and r.get("live")}
        for name in self.match_names():
            if name in sent_to or name not in liked or remaining["messages"] <= 0:
                continue
            choice = plan.choose_template(cfg["templates"], history, liked[name], self.rng)
            if choice is None:
                continue
            self.open_conversation(name)
            self.type_and_send(choice[1])
            self.record("message", liked[name], "first message", choice[0], choice[1])
            history.append(choice[0])
            remaining["messages"] -= 1
            done_messages += 1
            self.gap()
        self.collect_replies()
        return done_likes, done_messages

    def collect_replies(self):
        """Open every conversation this tool started and record each one the other side has answered, once."""
        rows = plan.read_ledger(self.ledger_path)
        answered = {r["profile"].get("name") for r in rows if r.get("action") == "reply" and r.get("live")}
        for r in rows:
            if r.get("action") != "message" or not r.get("live") or r["profile"].get("name") in answered:
                continue
            name = r["profile"]["name"]
            self.open_conversation(name)
            if any(not m["sent"] for m in self.messages()):
                self.record("reply", r["profile"], "the other side answered", r.get("template_id"))
                answered.add(name)
