import subprocess
import time
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

class RelaunchWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Relaunch & Restart Logic")
        self.resize(500, 280)

        self.exe_input = LoggedLineEdit()
        self.args_input = LoggedLineEdit()
        self.delay_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")
        self.status_label = QLabel("Status: Idle")

        self.args_input.setPlaceholderText("Optional arguments")
        self.delay_input.setPlaceholderText("Delay between restarts (seconds)")
        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(QLabel("Restart Delay"))
        layout.addWidget(self.delay_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

        self.process = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_process)

    def on_path_changed(self, text):
        self.run_btn.setEnabled(bool(text.strip()))

    def run_exe(self):
        exe = self.exe_input.text().strip()
        self.args = self.args_input.text().split() if self.args_input.text() else []
        delay_text = self.delay_input.text().strip()
        self.delay = int(delay_text) if delay_text.isdigit() else 5

        try:
            self.launch_process()
        except Exception as e:
            speak("Failed to launch process")
            print("Error:", e)

    def launch_process(self):
        exe = self.exe_input.text().strip()
        self.process = subprocess.Popen([exe] + self.args)
        self.status_label.setText(f"Status: Running PID {self.process.pid}")
        speak(f"Process started with PID {self.process.pid}")
        self.timer.start(1000)

    def check_process(self):
        if self.process.poll() is not None:
            self.status_label.setText("Status: Process exited, restarting...")
            speak("Process crashed or exited. Restarting...")
            self.timer.stop()
            time.sleep(self.delay)
            self.launch_process()
