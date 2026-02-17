from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class ControlWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_control)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_control(self):
        self.start_process("cmd", ["/c", "control"])
        speak("Please Check the output sir.")

class ControlPWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_controlp)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_controlp(self):
        self.start_process("cmd", ["/c", "control", "printers"])
        speak("Please Check the output sir.")

class ControlFWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_controlf)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_controlf(self):
        self.start_process("cmd", ["/c", "control", "firewall.cpl"])
        speak("Please Check the output sir.")

class EventvwrWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_eventvwr)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_eventvwr(self):
        self.start_process("cmd", ["/c", "eventvwr"])
        speak("Please Check the output sir.")

class TaskmgrWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_taskmgr)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_taskmgr(self):
        self.start_process("cmd", ["/c", "taskmgr"])
        speak("Please Check the output sir.")

class RegeditWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_regedit)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_regedit(self):
        self.start_process("cmd", ["/c", "regedit"])
        speak("Please Check the output sir.")
