import subprocess
import psutil
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow

class ProcessTrackingWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Process Tracking")
        self.resize(480, 260)

        self.exe_input = LoggedLineEdit()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")
        self.status_label = QLabel("Status: Idle")

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
        layout.addWidget(self.status_label)

        self.process = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)

    def on_path_changed(self, text):
        self.run_btn.setEnabled(bool(text.strip()))

    def run_exe(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []

        try:
            self.process = subprocess.Popen([exe] + args)
            self.pid = self.process.pid
            speak(f"Process started with PID {self.pid}")
            self.status_label.setText(f"Status: Running (PID {self.pid})")
            self.timer.start(1000)  # Update every second
        except Exception as e:
            speak("Failed to launch process")
            print("Error:", e)

    def update_status(self):
        if self.process is None:
            return

        if self.process.poll() is not None:
            self.status_label.setText("Status: Process terminated")
            speak("Process has exited")
            self.timer.stop()
        else:
            try:
                proc = psutil.Process(self.pid)
                cpu = proc.cpu_percent(interval=None)
                mem = proc.memory_info().rss / (1024 * 1024)  # MB
                self.status_label.setText(
                    f"Status: Running | CPU: {cpu:.1f}% | Memory: {mem:.1f} MB"
                )
            except psutil.NoSuchProcess:
                self.status_label.setText("Status: Process crashed or exited")
                speak("Process crashed or exited unexpectedly")
                self.timer.stop()
