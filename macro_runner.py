import threading
import time
from pynput.keyboard import Controller


class MacroRunner:
    def __init__(self):
        self.running = False
        self.thread = None
        self.keyboard = Controller()

    def start(self, macros):
        if self.running or not macros:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self.run_macro,
            args=(macros,),
            daemon=True
        )
        self.thread.start()

    def stop(self):
        self.running = False

    def run_macro(self, macros):
        while self.running:
            for entry in macros:
                if not self.running:
                    return

                key = entry["key"]
                delay = entry["delay"]
                repeat = entry.get("repeat", -1)

                if repeat < 0:
                    # Loop forever until stopped
                    while self.running:
                        self.press_key(key)
                        time.sleep(delay)
                else:
                    # Finite repeat
                    for _ in range(repeat):
                        if not self.running:
                            return
                        self.press_key(key)
                        time.sleep(delay)

    def press_key(self, key):
        try:
            self.keyboard.press(key)
            self.keyboard.release(key)
        except Exception:
            pass
