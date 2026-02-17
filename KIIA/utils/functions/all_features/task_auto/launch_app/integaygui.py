import subprocess
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow

class GUIIntegrationWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("GUI Integration Launcher")
        self.resize(450, 220)

        self.exe_input = LoggedLineEdit()
        self.run_btn = QPushButton("Launch")
        self.status_label = QLabel("Status: Idle")

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

        self.process = None

    def on_path_changed(self, text):
        self.run_btn.setEnabled(bool(text.strip()))

    def run_exe(self):
        exe = self.exe_input.text().strip()

        if not exe:
            self.status_label.setText("Status: No executable provided")
            speak("No executable path provided")
            return

        try:
            self.run_btn.setEnabled(False)
            self.status_label.setText("Status: Running...")
            self.process = subprocess.Popen([exe])
            speak("Process started")

            self.timer = QTimer()
            self.timer.timeout.connect(self.check_process)
            self.timer.start(500)

        except Exception as e:
            self.status_label.setText("Status: Failed to launch")
            speak("Failed to launch executable")
            print("Error:", e)
            self.run_btn.setEnabled(True)

    def check_process(self):
        if self.process.poll() is not None:
            self.status_label.setText("Status: Completed")
            speak("Process finished")
            self.run_btn.setEnabled(True)
            self.timer.stop()
