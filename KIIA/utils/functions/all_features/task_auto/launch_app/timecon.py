import subprocess
import time
import sched
import threading
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

class TimeControlWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Time-Based Execution Control")
        self.resize(500, 300)

        self.exe_input = LoggedLineEdit()
        self.args_input = LoggedLineEdit()
        self.delay_input = LoggedLineEdit()
        self.repeat_input = LoggedLineEdit()
        self.run_btn = QPushButton("Schedule")
        self.status_label = QLabel("Status: Idle")

        self.args_input.setPlaceholderText("Optional arguments")
        self.delay_input.setPlaceholderText("Delay before start (seconds)")
        self.repeat_input.setPlaceholderText("Repeat interval (seconds, 0 = once)")
        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.run_btn.clicked.connect(self.schedule_execution)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(QLabel("Delay Start"))
        layout.addWidget(self.delay_input)
        layout.addWidget(QLabel("Repeat Interval"))
        layout.addWidget(self.repeat_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = None

    def on_path_changed(self, text):
        self.run_btn.setEnabled(bool(text.strip()))

    def schedule_execution(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []
        delay = int(self.delay_input.text()) if self.delay_input.text().isdigit() else 0
        repeat = int(self.repeat_input.text()) if self.repeat_input.text().isdigit() else 0

        def run_process():
            try:
                subprocess.Popen([exe] + args)
                speak(f"Executed {exe}")
                self.status_label.setText(f"Status: Launched {exe}")
            except Exception as e:
                speak("Failed to execute scheduled process")
                print("Error:", e)
            if repeat > 0:
                self.scheduler.enter(repeat, 1, run_process)

        self.scheduler.enter(delay, 1, run_process)

        def scheduler_thread():
            self.scheduler.run()

        self.thread = threading.Thread(target=scheduler_thread, daemon=True)
        self.thread.start()
        speak("Process scheduled")
        self.status_label.setText("Status: Scheduler running")
