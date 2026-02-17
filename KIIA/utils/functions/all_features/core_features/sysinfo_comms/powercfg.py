from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class PowerCfgWindow(CommandWindow):
    def __init__(self, controller, title, powercfgs_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.systeminfo_args = powercfgs_args

        self.setWindowTitle("Lists all power schemes")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_powercfg)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_powercfg(self):
        self.start_process("cmd", ["/c", "powercfg"] + self.powercfgs_args)
        speak("Please Check the output sir.")

class PowerCFGMenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("SystemInfo Command Menu")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a SystemInfo command:"))

        self.commands = {
            "List Power Schemes": ["/list"],
            "Query Power Scheme": ["/query"],
            "Show Aliases": ["/aliases"],
            "Available Sleep States": ["/availablesleepstates"],
            "Last Wake Source": ["/lastwake"],
            "Battery Report": ["/batteryreport"],
            "Sleep Study Report": ["/sleepstudy"],
            "System Sleep Diagnostics": ["/systemsleepdiagnostics"],
            "System Power Report": ["/systempowereport"],
        }

        for title, args in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(lambda _, t=title, a=args: self.launch_command(t, a))
            layout.addWidget(btn)

    def launch_command(self, title, args):
        window = PowerCfgWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()