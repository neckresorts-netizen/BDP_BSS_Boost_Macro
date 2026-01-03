import json
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem,
    QLabel, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt
from pynput import keyboard
from pynput.keyboard import GlobalHotKeys

from macro_runner import MacroRunner
from settings_dialog import SettingsDialog

CONFIG_FILE = "config.json"


class MacroRow(QWidget):
    def __init__(self, entry, edit_callback):
        super().__init__()
        self.entry = entry
        self.edit_callback = edit_callback

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self.label = QLabel(self.text())
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedWidth(32)

        edit_btn.clicked.connect(self.edit_callback)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(edit_btn)

    def text(self):
        repeat = self.entry.get("repeat", -1)
        rep_text = "Loop" if repeat < 0 else f"x{repeat}"
        return f'{self.entry["key"]} | {self.entry["delay"]} s | {rep_text}'

    def refresh(self):
        self.label.setText(self.text())


class MacroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macro Editor")
        self.resize(520, 380)

        self.runner = MacroRunner()
        self.macros = []
        self.start_key = "f5"
        self.stop_key = "f6"

        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.settings_btn = QPushButton("Settings")
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")

        btns.addWidget(self.add_btn)
        btns.addWidget(self.settings_btn)
        btns.addStretch()
        btns.addWidget(self.start_btn)
        btns.addWidget(self.stop_btn)

        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(btns)

        self.add_btn.clicked.connect(self.add_key)
        self.start_btn.clicked.connect(self.start_macro)
        self.stop_btn.clicked.connect(self.stop_macro)
        self.settings_btn.clicked.connect(self.open_settings)

        self.load_config()
        self.setup_hotkeys()

    # ---------- Settings ----------
    def open_settings(self):
        dlg = SettingsDialog(self.start_key, self.stop_key)
        if dlg.exec():
            self.start_key, self.stop_key = dlg.get_keys()
            self.setup_hotkeys()
            self.save_config()

    def setup_hotkeys(self):
        try:
            self.hotkeys.stop()
        except Exception:
            pass

        self.hotkeys = GlobalHotKeys({
            f"<{self.start_key}>": self.start_macro,
            f"<{self.stop_key}>": self.stop_macro
        })
        self.hotkeys.start()

    # ---------- Add / Edit ----------
    def add_key(self):
        QMessageBox.information(self, "Add", "Press a key")

        def listen():
            def on_press(k):
                try:
                    key = k.char
                except AttributeError:
                    key = str(k).replace("Key.", "")

                entry = {"key": key, "delay": 0.5, "repeat": -1}
                self.macros.append(entry)
                self.refresh()
                self.save_config()
                return False

            with keyboard.Listener(on_press=on_press) as l:
                l.join()

        threading.Thread(target=listen, daemon=True).start()

    def edit_entry(self, entry, row_widget):
        delay, ok = QInputDialog.getDouble(
            self, "Delay", "Seconds:", entry["delay"], 0.0, 60.0, 2
        )
        if not ok:
            return

        repeat, ok = QInputDialog.getInt(
            self, "Repeat",
            "-1 = loop forever",
            entry.get("repeat", -1),
            -1, 9999
        )
        if not ok:
            return

        entry["delay"] = delay
        entry["repeat"] = repeat
        row_widget.refresh()
        self.save_config()

    # ---------- Macro ----------
    def start_macro(self):
        self.runner.start(self.macros)

    def stop_macro(self):
        self.runner.stop()

    # ---------- UI ----------
    def refresh(self):
        self.list_widget.clear()
        for entry in self.macros:
            item = QListWidgetItem()
            row = MacroRow(
                entry,
                lambda e=entry, r=None: self.edit_entry(e, r)
            )
            row.edit_callback = lambda e=entry, r=row: self.edit_entry(e, r)
            item.setSizeHint(row.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, row)

    # ---------- Save / Load ----------
    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.macros = data.get("macros", [])
                self.start_key = data.get("start_key", "f5")
                self.stop_key = data.get("stop_key", "f6")
                self.refresh()
        except FileNotFoundError:
            pass

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({
                "start_key": self.start_key,
                "stop_key": self.stop_key,
                "macros": self.macros
            }, f, indent=2)


if __name__ == "__main__":
    app = QApplication([])
    window = MacroApp()
    window.show()
    app.exec()
