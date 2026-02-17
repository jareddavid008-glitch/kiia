from PyQt6.QtWidgets import (
    QPushButton, QWidget,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class WmicWindow(CommandWindow):
    def __init__(self, controller, title, wmic_args, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.wmic_args = wmic_args

        self.setWindowTitle("Queries Windows Management Instrumentation.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_wmic)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_wmic(self):
        self.start_process("cmd", ["/c", "wmic"] + self.wmic_args)
        self.process.finished.connect(self.on_finished)
        speak("Please Check the output sir.")
    
    def on_finished(self):
        self.label.setText("Done")
        speak("Successful")
        QTimer.singleShot(1200, self.close)

class WmicSubMenu(QWidget):
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
        win = WmicWindow(self.controller, title, args)
        self.windows.append(win)
        win.show()

class WmicMenuWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.windows = []

        self.setWindowTitle("Wmic Command Menu")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a Wmic command:"))

        self.commands = {
            "System": {
                "Operating System": ["os", "get", "Caption,Version,BuildNumber"],
                "Computer System": ["computersystem", "get", "Name,Manufacturer,Model,Username"],
                "Boot Configuration": ["bootconfig", "get", "BootDirectory,ConfigurationPath"],
                "Time Zone": ["timezone", "get", "Caption,Bias"],
            },

            "Hardware": {
                "CPU Info": ["cpu", "get", "Name,NumberOfCores,MaxClockSpeed"],
                "BIOS Info": ["bios", "get", "Manufacturer,SMBIOSBIOSVersion"],
                "Baseboard (Motherboard)": ["baseboard", "get", "Manufacturer,Product,SerialNumber"],
                "Memory Modules": ["memorychip", "get", "Capacity,Speed,Manufacturer"],
            },

            "Storage": {
                "Disk Drives": ["diskdrive", "get", "Model,Size,InterfaceType"],
                "Logical Disks": ["logicaldisk", "get", "Name,FileSystem,FreeSpace,Size"],
                "Partitions": ["partition", "get", "Name,Size,Bootable"],
            },

            "Network": {
                "Network Adapters": ["nic", "where", "NetEnabled=true", "get", "Name,MACAddress"],
                "IP Configuration": ["nicconfig", "where", "IPEnabled=true", "get", "IPAddress,DefaultIPGateway"],
            },

            "Users & Sessions": {
                "Local User Accounts": ["useraccount", "get", "Name,Disabled,Lockout"],
                "Groups": ["group", "get", "Name"],
                "Logon Sessions": ["logonsession", "get", "LogonId,StartTime"],
            },

            "Software": {
                "Installed Products (Slow)": ["product", "get", "Name,Version"],
                "Services": ["service", "get", "Name,State,StartMode"],
                "Startup Programs": ["startup", "get", "Name,Command"],
            }
        }

        for category, subcommands in self.commands.items():
            btn = QPushButton(category)
            btn.clicked.connect(
                lambda _, c=category, s=subcommands: self.open_submenu(c, s)
            )
            layout.addWidget(btn)
    
    def open_submenu(self, category, subcommands):
        submenu = WmicSubMenu(self.controller, category, subcommands)
        self.windows.append(submenu)
        submenu.show()
            
    def launch_command(self, title, args):
        window = WmicWindow(self.controller, title, args)
        self.windows.append(window)
        window.show()