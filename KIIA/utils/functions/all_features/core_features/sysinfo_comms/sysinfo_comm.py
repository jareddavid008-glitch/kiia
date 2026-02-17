from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow

class HostNameWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("HostName Information")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display hostname information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_hostname)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_hostname(self):
        self.start_process("cmd", ["/c", "hostname"])
        speak("Please Check the output sir.")

class VerWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Shows Windows version")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_ver)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_ver(self):
        self.start_process("cmd", ["/c", "ver"])
        speak("Please Check the output sir.")

class TaskListWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Lists running processes")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_tasklist)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_tasklist(self):
        self.start_process("cmd", ["/c", "tasklist"])
        speak("Please Check the output sir.")

class TaskKillWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Terminates processes")
        self.resize(400, 100)

        self.input = LoggedLineEdit()
        self.btn = QPushButton("Kill")
        self.btn.clicked.connect(self.taskkill)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("File path"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def taskkill(self):
        process_name = self.input.text().strip()

        if not process_name:
            speak("Process name required")
            return

        self.start_process("cmd",["/c", "taskkill", "/IM", process_name, "/F"])
        speak("Please check the output sir.")
