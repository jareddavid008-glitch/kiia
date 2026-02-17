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

ENV_MODES = {
    "Inherit Current Environment": "inherit",
    "Override Variable": "override",
    "Inject Custom Variable": "inject"
}

class EnvironmentControlWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Environment Variable Control")
        self.resize(500, 320)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.var_input = LoggedLineEdit()
        self.value_input = LoggedLineEdit()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(ENV_MODES.keys())
        self.mode_select.setEnabled(False)

        self.var_input.setPlaceholderText("Variable Name (e.g. MY_VAR)")
        self.value_input.setPlaceholderText("Variable Value")
        self.args_input.setPlaceholderText("Optional arguments")

        self.var_input.setVisible(False)
        self.value_input.setVisible(False)
        self.args_input.setVisible(False)

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.mode_select.currentTextChanged.connect(self.on_mode_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Environment Mode"))
        layout.addWidget(self.mode_select)
        layout.addWidget(QLabel("Variable Name"))
        layout.addWidget(self.var_input)
        layout.addWidget(QLabel("Variable Value"))
        layout.addWidget(self.value_input)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(self.run_btn)

    def on_path_changed(self, text):
        valid = bool(text.strip())
        self.mode_select.setEnabled(valid)
        self.run_btn.setEnabled(valid)

    def on_mode_changed(self, mode):
        selected = ENV_MODES[mode]

        if selected == "inherit":
            self.var_input.setVisible(False)
            self.value_input.setVisible(False)
        else:
            self.var_input.setVisible(True)
            self.value_input.setVisible(True)

        self.args_input.setVisible(True)

    def run_exe(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []
        mode = ENV_MODES[self.mode_select.currentText()]

        try:
            if mode == "inherit":
                subprocess.Popen([exe] + args)
                speak("Application launched with inherited environment")

            else:
                env = os.environ.copy()

                var_name = self.var_input.text().strip()
                var_value = self.value_input.text().strip()

                if not var_name:
                    speak("Variable name required")
                    return
                
                env[var_name] = var_value

                subprocess.Popen([exe] + args, env=env)

                if mode == "override":
                    speak("Environment variable overridden")

                elif mode == "inject":
                    speak("Custom environment variable injected")

        except Exception as e:
            speak("Failed to launch with environment settings")
            print(f"Error: {e}")

        QTimer.singleShot(200, self.close)
