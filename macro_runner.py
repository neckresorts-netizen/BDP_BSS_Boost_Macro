import threading
import time
from pynput.keyboard import Controller

keyboard = Controller()


class MacroRunner:
    def __init__(self):
        self.threads = []
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.update_callback = None

    def set_update_callback(self, callback):
        self.update_callback = callback

    def start(self, macros):
        self.stop()
        self.stop_event.clear()
        self.pause_event.set()
        self.threads = []

        for entry in macros:
            t = threading.Thread(
                target=self.run_macro,
                args=(entry,),
                daemon=True
            )
            t.start()
            self.threads.append(t)

    def stop(self):
        self.stop_event.set()
        self.pause_event.set()

    def pause(self):
        self.pause_event.clear()

    def resume(self):
        self.pause_event.set()

    def run_macro(self, entry):
        delay = entry["delay"]
        repeat = entry["repeat"]

        count = 0
        while not self.stop_event.is_set():
            if repeat >= 0 and count >= repeat:
                break

            # ---------- PAUSE SAFE ----------
            self.pause_event.wait()
            if self.stop_event.is_set():
                break

            # ---------- INTERRUPTIBLE DELAY ----------
            remaining = delay
            start = time.time()

            while remaining > 0:
                if self.stop_event.is_set():
                    return

                self.pause_event.wait()
                step = min(0.05, remaining)
                if self.stop_event.wait(step):
                    return

                remaining = delay - (time.time() - start)

                if self.update_callback:
                    self.update_callback(entry, max(0, remaining))

            # ---------- PRESS KEY ----------
            if self.stop_event.is_set():
                return

            try:
                keyboard.press(entry["key"])
                keyboard.release(entry["key"])
            except Exception:
                pass

            if self.update_callback:
                self.update_callback(entry, None)

            count += 1
