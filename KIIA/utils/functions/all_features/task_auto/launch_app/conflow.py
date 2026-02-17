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

FLOW_MODES = {
    "Wait for Completion": "wait",
    "Get Exit Code": "exit_code",
    "Kill if Hangs (5s Timeout)": "kill_timeout"
}

class ExecutionFlowWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Execution Flow Control")
        self.resize(460, 270)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(FLOW_MODES.keys())
        self.mode_select.setEnabled(False)

        self.args_input.setPlaceholderText("Optional arguments")
        self.args_input.setVisible(False)

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.mode_select.currentTextChanged.connect(self.on_mode_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Execution Mode"))
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
        args = self.args_input.text().split() if self.args_input.text() else []
        mode = FLOW_MODES[self.mode_select.currentText()]

        try:
            process = subprocess.Popen([exe] + args)

            if mode == "wait":
                process.wait()
                speak("Application finished execution")

            elif mode == "exit_code":
                process.wait()
                code = process.returncode
                speak(f"Application exited with code {code}")

            elif mode == "kill_timeout":
                try:
                    process.wait(timeout=5)
                    speak("Application completed within time")
                except subprocess.TimeoutExpired:
                    speak("Application hung. Terminating.")
                    process.terminate()

                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        speak("Force killing process.")
                        process.kill()

        except Exception as e:
            speak("Failed to control process")
            print(f"Error: {e}")

        QTimer.singleShot(200, self.close)
