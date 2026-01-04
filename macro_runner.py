import threading
import time
from pynput.keyboard import Controller


class MacroRunner:
    def __init__(self):
        self.keyboard = Controller()
        self.threads = []
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()  # not paused initially
        self.lock = threading.Lock()

    # ---------- Start ----------
    def start(self, macros):
        """
        macros: list of dicts
        { key, delay, repeat, enabled }
        """
        self.stop()  # HARD STOP anything already running

        self.stop_event.clear()
        self.pause_event.set()
        self.threads.clear()

        for macro in macros:
            if not macro.get("enabled", True):
                continue

            t = threading.Thread(
                target=self._run_macro,
                args=(macro,),
                daemon=True
            )
            self.threads.append(t)
            t.start()

    # ---------- Worker ----------
    def _run_macro(self, macro):
        key = macro["key"]
        delay = float(macro["delay"])
        repeat = int(macro["repeat"])

        count = 0

        while not self.stop_event.is_set():
            self.pause_event.wait()  # pause support

            if self.stop_event.is_set():
                break

            # ---------- Press ----------
            with self.lock:
                self.keyboard.press(key)
                self.keyboard.release(key)

            count += 1

            if repeat >= 0 and count >= repeat:
                break

            # ---------- Delay ----------
            end_time = time.time() + delay
            while time.time() < end_time:
                if self.stop_event.is_set():
                    return
                time.sleep(0.01)

    # ---------- Controls ----------
    def stop(self):
        self.stop_event.set()
        self.pause_event.set()

        for t in self.threads:
            if t.is_alive():
                t.join(timeout=0.2)

        self.threads.clear()

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()
