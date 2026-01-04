import threading
import time
from pynput.keyboard import Controller
from PySide6.QtCore import QObject, Signal


class MacroRunner(QObject):
    tick = Signal(str, float)     # key, seconds_left
    fired = Signal(str)           # key pressed
    stopped = Signal()

    def __init__(self):
        super().__init__()
        self.keyboard = Controller()
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.thread = None
        self.paused = False

    def start(self, macros):
        self.stop()

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

                        key = m["key"]
                        delay = m["delay"]
                        repeat = m["repeat"]

                        count = 0
                        while repeat < 0 or count < repeat:
                            self.pause_event.wait()
                            if self.stop_event.is_set():
                                return

                            # Countdown loop
                            remaining = delay
                            while remaining > 0:
                                if self.stop_event.is_set():
                                    return
                                self.pause_event.wait(0.1)
                                remaining -= 0.1
                                self.tick.emit(key, max(0, remaining))

                            # Fire key
                            try:
                                self.keyboard.press(key)
                                self.keyboard.release(key)
                            except Exception:
                                pass

                            self.fired.emit(key)
                            count += 1
            finally:
                self.stopped.emit()

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
