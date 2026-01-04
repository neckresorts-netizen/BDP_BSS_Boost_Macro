from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, start_key, stop_key, pause_key):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(320, 260)

        self.setStyleSheet("""
        QDialog {
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 14px;
        }
        QLabel {
            color: #bbbbbb;
        }
        QComboBox {
            background-color: #2a2a2a;
            padding: 6px;
            border-radius: 6px;
        }
        QPushButton {
            background-color: #3a3a3a;
            border-radius: 6px;
            padding: 8px 14px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(14, 14, 14, 14)

        title = QLabel("Hotkey Settings")
        title.setStyleSheet("font-size: 16px; font-weight:bold; color: white;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Start Macro"))
        self.start_combo = QComboBox()
        self.start_combo.addItems(self.function_keys())
        self.start_combo.setCurrentText(start_key)
        layout.addWidget(self.start_combo)

        layout.addWidget(QLabel("Pause Macro"))
        self.pause_combo = QComboBox()
        self.pause_combo.addItems(self.function_keys())
        self.pause_combo.setCurrentText(pause_key)
        layout.addWidget(self.pause_combo)

        layout.addWidget(QLabel("Stop Macro"))
        self.stop_combo = QComboBox()
        self.stop_combo.addItems(self.function_keys())
        self.stop_combo.setCurrentText(stop_key)
        layout.addWidget(self.stop_combo)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("Save")
        save_btn.setMinimumWidth(90)
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def function_keys(self):
        return [f"f{i}" for i in range(1, 13)]

    def get_keys(self):
        return (
            self.start_combo.currentText(),
            self.stop_combo.currentText(),
            self.pause_combo.currentText()
        )
