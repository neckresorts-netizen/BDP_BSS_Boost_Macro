from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, start_key, stop_key, pause_key):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setMinimumSize(380, 300)
        
        self.setStyleSheet("""
        QDialog {
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 14px;
        }
        QLabel {
            color: #bbbbbb;
            padding: 2px;
        }
        QComboBox {
            background-color: #2a2a2a;
            color: #ffffff;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid #3a3a3a;
            min-height: 24px;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
            margin-right: 8px;
        }
        QComboBox QAbstractItemView {
            background-color: #2a2a2a;
            color: #ffffff;
            selection-background-color: #3a3a3a;
            padding: 4px;
        }
        QPushButton {
            background-color: #3a3a3a;
            color: #ffffff;
            border-radius: 6px;
            padding: 10px 20px;
            border: none;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #606060;
        }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Hotkey Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; padding-bottom: 8px;")
        layout.addWidget(title)
        
        # Start Macro
        start_label = QLabel("Start Macro")
        start_label.setStyleSheet("font-size: 14px; color: #dddddd; font-weight: bold;")
        layout.addWidget(start_label)
        
        self.start_combo = QComboBox()
        self.start_combo.addItems(self.function_keys())
        self.start_combo.setCurrentText(start_key)
        self.start_combo.setMinimumWidth(120)
        layout.addWidget(self.start_combo)
        
        # Pause Macro
        pause_label = QLabel("Pause Macro")
        pause_label.setStyleSheet("font-size: 14px; color: #dddddd; font-weight: bold;")
        layout.addWidget(pause_label)
        
        self.pause_combo = QComboBox()
        self.pause_combo.addItems(self.function_keys())
        self.pause_combo.setCurrentText(pause_key)
        self.pause_combo.setMinimumWidth(120)
        layout.addWidget(self.pause_combo)
        
        # Stop Macro
        stop_label = QLabel("Stop Macro")
        stop_label.setStyleSheet("font-size: 14px; color: #dddddd; font-weight: bold;")
        layout.addWidget(stop_label)
        
        self.stop_combo = QComboBox()
        self.stop_combo.addItems(self.function_keys())
        self.stop_combo.setCurrentText(stop_key)
        self.stop_combo.setMinimumWidth(120)
        layout.addWidget(self.stop_combo)
        
        layout.addStretch()
        
        # Save Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.setMinimumWidth(100)
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
