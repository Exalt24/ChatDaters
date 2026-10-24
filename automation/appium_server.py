"""Start an Appium server as a child of this process and always stop it again.

The server is a child (no console window, nothing that outlives the run) and is stopped by the PID this module started, never by process name.
Readiness is polled on /status in short steps with a hard cap. The Chrome route needs the server to be allowed to fetch a matching chromedriver
for the emulator's Chrome, so that one insecure feature is switched on for this server only.

Needs: `npm install -g appium`, `appium driver install uiautomator2`, a booted emulator or a phone with USB debugging, and ANDROID_HOME set.
"""
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request

READY_TIMEOUT_S = 60
POLL_S = 0.25
_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def appium_command():
    found = shutil.which("appium") or shutil.which("appium.cmd")
    if found:
        return found
    roaming = os.environ.get("APPDATA")
    cand = os.path.join(roaming, "npm", "appium.cmd") if roaming else None
    return cand if cand and os.path.isfile(cand) else None


def _status(url):
    try:
        with urllib.request.urlopen(url + "/status", timeout=2) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except (urllib.error.URLError, OSError, ValueError):
        return None


class AppiumServer:
    def __init__(self, port=4723, log_path="appium_server.log"):
        self.port, self.log_path = port, log_path
        self.url = "http://127.0.0.1:%d" % port
        self.proc = None
        self._log = None

    def start(self):
        cmd = appium_command()
        if not cmd:
            raise RuntimeError("appium is not installed: npm install -g appium, then appium driver install uiautomator2")
        if _status(self.url):
            raise RuntimeError("something already answers on %s: stop it first, this module only owns a server it started" % self.url)
        self._log = open(self.log_path, "wb")
        self.proc = subprocess.Popen([cmd, "--port", str(self.port), "--log-no-colors", "--allow-insecure", "uiautomator2:chromedriver_autodownload"],
                                     stdout=self._log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=_NO_WINDOW)
        deadline = time.monotonic() + READY_TIMEOUT_S
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                raise RuntimeError("appium exited with code %s, see %s" % (self.proc.returncode, self.log_path))
            status = _status(self.url)
            if status and (status.get("value") or {}).get("ready", True):
                return self
            time.sleep(POLL_S)
        self.stop()
        raise RuntimeError("appium was not ready in %d s, see %s" % (READY_TIMEOUT_S, self.log_path))

    def stop(self):
        proc, self.proc = self.proc, None
        if proc is not None and proc.poll() is None:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, creationflags=_NO_WINDOW, timeout=30)
            else:
                proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
        if self._log:
            self._log.close()
            self._log = None

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.stop()
        return False
