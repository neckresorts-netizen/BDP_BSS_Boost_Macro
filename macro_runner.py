import threading
import time
from pynput.keyboard import Controller

keyboard_controller = Controller()


class MacroRunner:
    def __init__(self):
        self.threads = []
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.running = False
        self.update_callback = None  # UI hook

    def set_update_callback(self, callback):
        self.update_callback = callback

    def start(self, macros):
        self.stop()
        self.stop_event.clear()
        self.pause_event.set()
        self.running = True

        for entry in macros:
            t = threading.Thread(
                target=self.run_macro,
                args=(entry,),
                daemon=True
            )
            self.threads.append(t)
            t.start()

    def stop(self):
        self.running = False
        self.stop_event.set()
        self.pause_event.set()
        self.threads.clear()

    def pause(self):
        if self.running:
            self.pause_event.clear()

    def resume(self):
        if self.running:
            self.pause_event.set()

    def run_macro(self, entry):
        delay = entry["delay"]
        repeat = entry["repeat"]
        count = 0

        while not self.stop_event.is_set():
            if repeat >= 0 and count >= repeat:
                break

            remaining = delay

            while remaining > 0:
                if self.stop_event.is_set():
                    return

                self.pause_event.wait()

                step = min(0.05, remaining)
                time.sleep(step)
                remaining -= step

                if self.update_callback:
                    self.update_callback(entry, remaining)

            if self.stop_event.is_set():
                return

            self.pause_event.wait()

            keyboard_controller.press(entry["key"])
            keyboard_controller.release(entry["key"])

            if self.update_callback:
                self.update_callback(entry, None)  # reset display

            count += 1
