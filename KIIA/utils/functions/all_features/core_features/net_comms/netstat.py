from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class netstatWindow(CommandWindow):
    def __init__(self, controller, title, netstats_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.netstats_args = netstats_args

        self.setWindowTitle("Lists all power schemes")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_netstat)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_netstat(self):
        self.start_process("cmd", ["/c"] + self.netstats_args)
        self.process.finished.connect(self.on_finished)
        speak("Please Check the output sir.")
    
    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class NetstatWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("Netstat Command Menu")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a Netstat command:"))

        self.commands = {
            "Active Connections": ["netstat", "-a"],
            "Numerical Addresses": ["netstat", "-n"],
            "Connections + PID": ["netstat", "-o"],
            "Routing Table": ["netstat", "-r"],
            "Protocol Statistics": ["netstat", "-s"],
        }

        for title, args in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(lambda _, t=title, a=args: self.launch_command(t, a))
            layout.addWidget(btn)
            

    def launch_command(self, title, args):
        window = netstatWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()