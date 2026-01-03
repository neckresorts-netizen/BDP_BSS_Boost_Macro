from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QComboBox, QPushButton
)


class SettingsDialog(QDialog):
    def __init__(self, start_key, stop_key):
        super().__init__()
        self.setWindowTitle("Settings")

        self.start_key = start_key
        self.stop_key = stop_key

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Start Macro Key"))
        self.start_combo = QComboBox()
        self.start_combo.addItems(["f5", "f7", "f8", "f9"])
        self.start_combo.setCurrentText(start_key)
        layout.addWidget(self.start_combo)

        layout.addWidget(QLabel("Stop Macro Key"))
        self.stop_combo = QComboBox()
        self.stop_combo.addItems(["f6", "f7", "f8", "f9"])
        self.stop_combo.setCurrentText(stop_key)
        layout.addWidget(self.stop_combo)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

    def get_keys(self):
        return self.start_combo.currentText(), self.stop_combo.currentText()
