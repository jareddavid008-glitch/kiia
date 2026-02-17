from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class WhoAmIWindow(CommandWindow):
    def __init__(self, controller, title, whoami_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.whoami_args = whoami_args

        self.setWindowTitle("Shows current Logged In User")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_whoami)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_whoami(self):
        self.start_process("cmd", ["/c", "whoami"] + self.whoami_args)
        speak("Please Check the output sir.")

class WhoAmIMenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("WhoAmI Command Menu")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a WhoAmI command:"))

        self.commands = {
            "Current User": [],
            "User UPN": ["/upn"],
            "User FQDN": ["/fqdn"],
            "Logon ID": ["/logonid"],
            "User SID": ["/user"],
            "User SID (List)": ["/user", "/fo", "list"],
            "User SID (CSV)": ["/user", "/fo", "csv"],
            "Groups": ["/groups"],
            "Groups (CSV)": ["/groups", "/fo", "csv", "/nh"],
            "Claims": ["/claims"],
            "Claims (List)": ["/claims", "/fo", "list"],
            "Privileges": ["/priv"],
            "Privileges (Table)": ["/priv", "/fo", "table"],
            "All Information": ["/all"],
            "All Info (List)": ["/all", "/fo", "list"],
            "All Info (CSV)": ["/all", "/fo", "csv", "/nh"],
        }

        for title, args in self.commands.items():
            btn = QPushButton(title)
            btn.clicked.connect(lambda _, t=title, a=args: self.launch_command(t, a))
            layout.addWidget(btn)

    def launch_command(self, title, args):
        window = WhoAmIWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()
