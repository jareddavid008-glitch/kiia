from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer, QProcess
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class IpConfigWindow(CommandWindow):
    def __init__(self, controller, title, ipconfig_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.ipconfig_args = ipconfig_args

        self.setWindowTitle("Lists all power schemes")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_ipconfig)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_ipconfig(self):
        self.start_process("cmd", ["/c"] + self.ipconfig_args)
        self.process.finished.connect(self.on_finished)
        speak("Please Check the output sir.")
    
    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class IpConfigMenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("Ipconfig Command Menu")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a Ipconfig command:"))

        self.commands = {
            "IP Summary": ["ipconfig"],
            "IP Full Details": ["ipconfig", "/all"],
            "DNS Cache": ["ipconfig", "/displaydns"],
            "DHCP Class ID (IPv4)": ["ipconfig", "/showclassid"],
            "DHCP Class ID (IPv6)": ["ipconfig", "/showclassid6"],
            "All Compartments": ["ipconfig", "/allcompartments"],
            "All Compartments (Full)": ["ipconfig", "/allcompartments", "/all"],
        }

        for title, args in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(lambda _, t=title, a=args: self.launch_command(t, a))
            layout.addWidget(btn)
            
    def launch_command(self, title, args):
        window = IpConfigWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()