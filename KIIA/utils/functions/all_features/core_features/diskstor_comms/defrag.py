from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
from .....tools.logger import LoggedLineEdit
from ....allowed import SAFE_DEFRAG_COMMANDS

class DefragCommandWindow(CommandWindow):
    def __init__(self, controller, title, defrag_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.defrag_args = defrag_args

        self.setWindowTitle(title)
        self.resize(350, 100)

        speak("Gathering service information.")

        self.label = QLabel("Click execute to display service information")
        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_defrag)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_defrag(self):
        self.start_process("cmd", ["/c"] + self.defrag_args)
        self.process.finished.connect(self.on_finished)
        speak("Please check the output.")

    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class DefragInputWindow(CommandWindow):
    def __init__(self, controller, title, base_cmd, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.base_cmd = base_cmd

        self.setWindowTitle(title)
        self.resize(400, 140)

        self.label = QLabel("Enter Service Name (e.g. wuauserv)")
        self.input = LoggedLineEdit()
        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_defrag)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
    
    def run_defrag(self):
        service = self.input.text().strip()
        if not service:
            speak("Service name required")
            return

        self.start_process("cmd", ["/c"] + self.base_cmd + [service])
        self.process.finished.connect(self.on_finished)
        speak("Please Check the output sir.")
        
    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class DefragSafeMenu(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("Service Controller Menu")
        self.resize(400, 250)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select an Defrag command:"))

        self.commands = SAFE_DEFRAG_COMMANDS
        
        for title, spec in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(
                lambda _, t=title, s=spec: self.launch_command(t, s)
            )
            layout.addWidget(btn)

    def launch_command(self, title, spec):
        if not spec["input"]:
            win = DefragCommandWindow(self.controller, title, spec["cmd"])
        else:
            win = DefragInputWindow(self.controller, title, spec["cmd"])

        self.windows.append(win)
        win.show()
