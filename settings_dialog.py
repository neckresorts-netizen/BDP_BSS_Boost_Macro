from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QHBoxLayout
)


class SettingsDialog(QDialog):
    def __init__(self, start_key, stop_key):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(320, 220)

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
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Hotkey Settings")
        title.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Start Macro"))
        self.start_combo = QComboBox()
        self.start_combo.addItems(self.function_keys())
        self.start_combo.setCurrentText(start_key)
        layout.addWidget(self.start_combo)

        layout.addWidget(QLabel("Stop Macro"))
        self.stop_combo = QComboBox()
        self.stop_combo.addItems(self.function_keys())
        self.stop_combo.setCurrentText(stop_key)
        layout.addWidget(self.stop_combo)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("Save")
        save_btn.setMinimumHeight(36)
        save_btn.setStyleSheet("padding: 6px 16px;")
        save_btn.clicked.connect(self.accept)

        btn_layout.addWidget(save_btn)

        layout.addStretch()
        layout.addLayout(btn_layout)

    def function_keys(self):
        return [f"f{i}" for i in range(1, 13)]

    def get_keys(self):
        return (
            self.start_combo.currentText(),
            self.stop_combo.currentText()
        )
