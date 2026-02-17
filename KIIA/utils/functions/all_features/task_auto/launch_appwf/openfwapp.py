import os
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel
)
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow

class DefaultAppLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open File with Default App")
        self.resize(450, 200)

        self.file_input = LoggedLineEdit()
        self.run_btn = QPushButton("Open File")
        self.status_label = QLabel("Status: Idle")

        self.run_btn.setEnabled(False)

        self.file_input.textChanged.connect(self.on_path_changed)
        self.run_btn.clicked.connect(self.open_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("File path"))
        layout.addWidget(self.file_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def on_path_changed(self, text):
        self.run_btn.setEnabled(bool(text.strip()))

    def open_file(self):
        file_path = self.file_input.text().strip()

        if not file_path:
            self.status_label.setText("Status: No file provided")
            speak("Please provide a file path")
            return

        if not os.path.exists(file_path):
            self.status_label.setText("Status: File not found")
            speak("File does not exist")
            return

        try:
            os.startfile(file_path)
            self.status_label.setText(f"Status: Opened {os.path.basename(file_path)}")
            speak(f"Opened {os.path.basename(file_path)} successfully")
        except Exception as e:
            self.status_label.setText("Status: Failed to open file")
            speak("Failed to open file")
            print("Error:", e)
