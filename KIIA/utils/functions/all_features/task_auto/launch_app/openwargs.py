import subprocess
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

ARGUMENT_MODES = {
    "Open with File(s)": "files",
    "Open with Flags": "flags",
    "Open with Multiple Arguments": "multiple"
}

class OpenExeWithArgsWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Launch with Arguments")
        self.resize(450, 270)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(ARGUMENT_MODES.keys())
        self.mode_select.setEnabled(False)

        self.args_input.setPlaceholderText("Enter arguments (space separated)")
        self.args_input.setVisible(False)

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.mode_select.currentTextChanged.connect(self.on_mode_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Argument Mode"))
        layout.addWidget(self.mode_select)
        layout.addWidget(QLabel("Arguments / File Paths"))
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
        mode = ARGUMENT_MODES[self.mode_select.currentText()]
        args = self.args_input.text().split() if self.args_input.text() else []

        try:
            if mode == "files":
                subprocess.Popen([exe] + args)
                speak("Application opened with files")

            elif mode == "flags":
                subprocess.Popen([exe] + args)
                speak("Application launched with flags")

            elif mode == "multiple":
                subprocess.Popen([exe] + args)
                speak("Application launched with multiple arguments")

        except Exception as e:
            speak("Failed to launch application")
            print(f"Error: {e}")

        QTimer.singleShot(200, self.close)
