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

CWD_MODES = {
    "Set Startup Directory": "startup",
    "Load Config Relative to Folder": "config",
    "Control Logs / Files Location": "logs"
}

class WorkingDirectoryWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Working Directory Control")
        self.resize(480, 300)

        self.exe_input = LoggedLineEdit()
        self.cwd_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(CWD_MODES.keys())
        self.mode_select.setEnabled(False)

        self.cwd_input.setPlaceholderText("Working directory (e.g. C:\\AppFolder)")
        self.args_input.setPlaceholderText("Optional arguments")
        self.args_input.setVisible(False)

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.mode_select.currentTextChanged.connect(self.on_mode_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Working Directory"))
        layout.addWidget(self.cwd_input)
        layout.addWidget(QLabel("Mode"))
        layout.addWidget(self.mode_select)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(self.run_btn)

    def on_path_changed(self, text):
        valid = bool(text.strip())
        self.mode_select.setEnabled(valid)
        self.run_btn.setEnabled(valid)

    def on_mode_changed(self, mode):
        self.args_input.setVisible(True)

    def run_exe(self):
        exe = self.exe_input.text().strip()
        cwd = self.cwd_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []
        mode = CWD_MODES[self.mode_select.currentText()]

        try:
            if not os.path.isdir(cwd):
                speak("Invalid working directory")
                return

            if mode == "startup":
                subprocess.Popen([exe] + args, cwd=cwd)
                speak("Application started with custom startup directory")

            elif mode == "config":
                subprocess.Popen([exe] + args, cwd=cwd)
                speak("Application loading config from working folder")

            elif mode == "logs":
                subprocess.Popen([exe] + args, cwd=cwd)
                speak("Application logs will be written to working folder")

        except Exception as e:
            speak("Failed to launch with working directory")
            print(f"Error: {e}")

        QTimer.singleShot(200, self.close)
