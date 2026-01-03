import json
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QInputDialog, QMessageBox
)
from macro_runner import MacroRunner
from key_listener import listen_for_single_key

CONFIG_FILE = "config.json"

class MacroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macro Editor")

        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.add_button = QPushButton("Add Key")
        self.remove_button = QPushButton("Remove Selected")

        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)

        self.macro_runner = MacroRunner()
        self.macros = []

        self.add_button.clicked.connect(self.add_key)
        self.remove_button.clicked.connect(self.remove_key)

        self.load_config()

    def add_key(self):
        QMessageBox.information(self, "Key", "Press a key to add")
        def got_key(key):
            delay, ok = QInputDialog.getInt(self, "Delay", "Delay (ms):", 100)
            if ok:
                entry = {"key": key, "delay": delay}
                self.macros.append(entry)
                self.list_widget.addItem(f"{key} | {delay} ms")
                self.save_config()
        listen_for_single_key(got_key)

    def remove_key(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)
            self.macros.pop(row)
            self.save_config()

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.macros = data["macros"]
                for m in self.macros:
                    self.list_widget.addItem(f"{m['key']} | {m['delay']} ms")
        except FileNotFoundError:
            pass

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({
                "start_key": "f5",
                "stop_key": "f6",
                "macros": self.macros
            }, f, indent=2)

if __name__ == "__main__":
    app = QApplication([])
    window = MacroApp()
    window.show()
    app.exec()
