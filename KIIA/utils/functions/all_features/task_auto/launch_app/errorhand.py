import subprocess
import os
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel,
    QComboBox
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow

class ErrorHandlingWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Error Handling & Validation")
        self.resize(480, 240)

        self.exe_input = LoggedLineEdit()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.args_input.setPlaceholderText("Optional arguments")
        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(self.run_btn)

    def on_path_changed(self, text):
        self.run_btn.setEnabled(bool(text.strip()))

    def run_exe(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []

        if not exe:
            speak("Executable path is missing")
            return

        if not os.path.exists(exe):
            speak("Executable file does not exist")
            return

        if not os.access(exe, os.X_OK):
            speak("You do not have permission to execute this file")
            return

        try:
            process = subprocess.run([exe] + args)
            if process.returncode != 0:
                speak(f"Process exited with code {process.returncode}")
            else:
                speak("Process executed successfully")
        except FileNotFoundError:
            speak("File not found error")
        except PermissionError:
            speak("Permission denied error")
        except Exception as e:
            speak("An unexpected error occurred")
            print("Error:", e)

        QTimer.singleShot(200, self.close)
