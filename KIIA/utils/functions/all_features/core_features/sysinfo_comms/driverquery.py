from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer, QProcess
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class DriverQueryWindow(CommandWindow):
    def __init__(self, controller, title, driverquery_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.driverquery_args = driverquery_args

        self.setWindowTitle("Lists installed drivers.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_driverquery)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_driverquery(self):
        self.start_process("cmd", ["/c"] + self.driverquery_args)
        self.process.finished.connect(self.on_finished)
        speak("Please Check the output sir.")
    
    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class DriverQuerySubMenu(QWidget):
    def __init__(self, controller, category, commands):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle(category)
        self.resize(400, 200)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{category} Commands"))

        for title, args in commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(
                lambda _, t=title, a=args: self.launch_command(t, a)
            )
            layout.addWidget(btn)

    def launch_command(self, title, args):
        win = DriverQueryWindow(self.controller, title, args)
        self.windows.append(win)
        win.show()

class DriverQueryMenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("DriverQuery Command Menu")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a DriverQuery command:"))

        self.commands = {
            "Basic": {
                "Loaded Drivers (Table)": ["driverquery"],
                "Loaded Drivers (No Header)": ["driverquery", "/NH"],
            },

            "Detailed": {
                "Verbose Driver Info": ["driverquery", "/V"],
                "Verbose (No Header)": ["driverquery", "/V", "/NH"],
            },

            "Security": {
                "Signed Drivers (CSV)": ["driverquery", "/FO", "CSV", "/SI"],
                "Signed Drivers (Table)": ["driverquery", "/SI"],
            },

            "Formats": {
                "Driver List (CSV)": ["driverquery", "/FO", "CSV"],
                "Driver List (LIST)": ["driverquery", "/FO", "LIST"],
            }
        }

        for category, subcommands in self.commands.items():
            btn = QPushButton(category)
            btn.clicked.connect(
                lambda _, c=category, s=subcommands: self.open_submenu(c, s)
            )
            layout.addWidget(btn)
    
    def open_submenu(self, category, subcommands):
        submenu = DriverQuerySubMenu(self.controller, category, subcommands)
        self.windows.append(submenu)
        submenu.show()
            
    def launch_command(self, title, args):
        window = DriverQueryWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()