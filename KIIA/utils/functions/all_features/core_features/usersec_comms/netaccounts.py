from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
from .....tools.logger import LoggedLineEdit
from ....allowed import SAFE_NET_ACCOUNTS_COMMANDS

class NetaccountsCommandWindow(CommandWindow):
    def __init__(self, controller, title, netaccounts_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.netaccounts_args = netaccounts_args

        self.setWindowTitle(title)
        self.resize(350, 100)

        speak("Gathering service information.")

        self.label = QLabel("Click execute to display service information")
        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_netaccounts)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_netaccounts(self):
        self.start_process("cmd", ["/c"] + self.netaccounts_args)
        self.process.finished.connect(self.on_finished)
        speak("Please check the output.")

    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class NetaccountsInputWindow(CommandWindow):
    def __init__(self, controller, title, base_cmd, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.base_cmd = base_cmd

        self.setWindowTitle(title)
        self.resize(400, 140)

        self.label = QLabel("Enter Service Name (e.g. wuauserv)")
        self.input = LoggedLineEdit()
        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_netaccounts)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
    
    def run_netaccounts(self):
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

class NetaccountsSafeMenu(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("Service Controller Menu")
        self.resize(400, 250)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select an Net Accounts command:"))

        self.commands = SAFE_NET_ACCOUNTS_COMMANDS
        
        for title, spec in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(
                lambda _, t=title, s=spec: self.launch_command(t, s)
            )
            layout.addWidget(btn)

    def launch_command(self, title, spec):
        if not spec["input"]:
            win = NetaccountsCommandWindow(self.controller, title, spec["cmd"])
        else:
            win = NetaccountsInputWindow(self.controller, title, spec["cmd"])

        self.windows.append(win)
        win.show()
