import threading
import time
from pynput.keyboard import Controller, Key


class MacroRunner:
    def __init__(self):
        self.keyboard = Controller()
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.thread = None
        self.paused = False

    def start(self, macros):
        self.stop()  # HARD STOP anything existing

        self.stop_event.clear()
        self.pause_event.set()
        self.paused = False

        def run():
            try:
                while not self.stop_event.is_set():
                    for m in macros:
                        if self.stop_event.is_set():
                            return

                        if not m.get("enabled", True):
                            continue

                        # PAUSE BLOCK
                        self.pause_event.wait()
                        if self.stop_event.is_set():
                            return

                        key = m["key"]
                        repeat = m["repeat"]
                        delay = m["delay"]

                        count = 0
                        while repeat < 0 or count < repeat:
                            if self.stop_event.is_set():
                                return

                            self.pause_event.wait()

                            try:
                                self.keyboard.press(key)
                                self.keyboard.release(key)
                            except Exception:
                                pass

                            count += 1

                            # INTERRUPTIBLE DELAY
                            end = time.time() + delay
                            while time.time() < end:
                                if self.stop_event.is_set():
                                    return
                                self.pause_event.wait(0.05)
            finally:
                self.stop_event.set()

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def pause(self):
        self.paused = True
        self.pause_event.clear()

    def resume(self):
        self.paused = False
        self.pause_event.set()

    def stop(self):
        self.stop_event.set()
        self.pause_event.set()

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)

        self.thread = None
