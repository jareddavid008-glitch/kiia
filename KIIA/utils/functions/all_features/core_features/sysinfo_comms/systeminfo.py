from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class SystemInfoWindow(CommandWindow):
    def __init__(self, controller, title, systeminfo_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.systeminfo_args = systeminfo_args

        self.setWindowTitle("System Information")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_systeminfo)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_systeminfo(self):
        self.start_process("cmd", ["/c", "systeminfo"] + self.systeminfo_args)
        speak("Please Check the output sir.")

class SystemInfoMenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("SystemInfo Command Menu")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a SystemInfo command:"))

        self.commands = {
            "Local System Info": [],
            "Remote System": ["/S", "system"],
            "Remote System (User)": ["/S", "system", "/U", "user"],
            "Remote System (Creds, Table)": [
                "/S", "system", "/U", "domain\\user", "/P", "password", "/FO", "TABLE"
            ],
            "Local Info (List)": ["/FO", "LIST"],
            "Local Info (CSV, No Header)": ["/FO", "CSV", "/NH"],
        }

        for title, args in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(lambda _, t=title, a=args: self.launch_command(t, a))
            layout.addWidget(btn)

    def launch_command(self, title, args):
        window = SystemInfoWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()