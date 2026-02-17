from PyQt6.QtWidgets import (
    QWidget, QPushButton,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer, QProcess
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow
from .....tools.admin_verif import check_and_execute

import os

class DirWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Directory Listing")
        self.resize(400, 100)

        speak("Please enter the directory path.")

        self.label = QLabel("Enter directory path")
        self.input = LoggedLineEdit()
        self.input.setPlaceholderText("Leave empty for current directory")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_dir)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def run_dir(self):
        path = self.input.text().strip() or "."
        check_and_execute(self, "cmd", ["/c", "dir", path])
        speak("Please Check the output sir.")

class SearchFile(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Search File")
        self.resize(400, 100)

        speak("Please enter the directory path.")

        self.label = QLabel("Enter directory path")
        self.input = LoggedLineEdit()
        self.input.setPlaceholderText("Leave empty for current directory")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_dirs)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def run_dirs(self):
        path = self.input.text().strip() or "."
        self.start_process("cmd", ["/c", "dir", path, "/s"])
        speak("Please Check the output sir.")

class CopyWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Copy File")
        self.resize(300, 150)

        speak("Please enter source and destination.")

        self.src_input = LoggedLineEdit()
        self.dst_input = LoggedLineEdit()

        self.btn = QPushButton("Copy")
        self.btn.clicked.connect(self.copy_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Source file"))
        layout.addWidget(self.src_input)
        layout.addWidget(QLabel("Destination file"))
        layout.addWidget(self.dst_input)
        layout.addWidget(self.btn)

    def copy_file(self):
        src = self.src_input.text().strip()
        dst = self.dst_input.text().strip()

        if not src or not dst:
            speak("Source and destination required")
            return

        speak("Copying file.")
        self.start_process("cmd", ["/c", "copy", src, dst])
        speak("Please Check the output sir.")

class MoveWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Move File")
        self.resize(300, 150)

        self.src_input = LoggedLineEdit()
        self.dst_input = LoggedLineEdit()

        self.btn = QPushButton("Move")
        self.btn.clicked.connect(self.move_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Source file"))
        layout.addWidget(self.src_input)
        layout.addWidget(QLabel("Destination file"))
        layout.addWidget(self.dst_input)
        layout.addWidget(self.btn)

    def move_file(self):
        src = self.src_input.text().strip()
        dst = self.dst_input.text().strip()

        if not src or not dst:
            speak("Source and destination required")
            return

        speak("Moving file.")
        self.start_process("cmd", ["/c", "move", src, dst])
        speak("Please Check the output sir.")

class DeldWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Delete File")
        self.resize(400, 100)

        self.input = LoggedLineEdit()
        self.btn = QPushButton("Delete")
        self.btn.clicked.connect(self.del_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter file path"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def del_file(self):
        path = self.input.text().strip()

        if not path:
            speak("File path required")
            return

        speak("Deleting file.")
        self.start_process("cmd", ["/c", "del", path])
        speak("Please Check the output sir.")

class MkDirWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Create Directory")
        self.resize(400, 100)

        self.input = LoggedLineEdit()
        self.btn = QPushButton("Create")
        self.btn.clicked.connect(self.mk_dir)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Directory name"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def mk_dir(self):
        path = self.input.text().strip()

        if not path:
            speak("Directory name required")
            return

        speak("Creating directory.")
        self.start_process("cmd", ["/c", "mkdir", path])
        speak("Please Check the output sir.")

class RmDirWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Remove Directory (Dangerous)")
        self.resize(400, 100)

        self.input = LoggedLineEdit()
        self.btn = QPushButton("Remove")
        self.btn.clicked.connect(self.rm_dir)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Directory path"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def rm_dir(self):
        path = self.input.text().strip()

        if not path:
            speak("Directory path required")
            return

        speak("Removing directory.")
        self.start_process("cmd", ["/c", "rmdir", path])
        speak("Please Check the output sir.")

class RenameWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Rename File")
        self.resize(300, 150)

        self.src_input = LoggedLineEdit()
        self.dst_input = LoggedLineEdit()
        self.btn = QPushButton("Rename")
        self.btn.clicked.connect(self.rename_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Source file"))
        layout.addWidget(self.src_input)
        layout.addWidget(QLabel("New name"))
        layout.addWidget(self.dst_input)
        layout.addWidget(self.btn)

    def rename_file(self):
        src = self.src_input.text().strip()
        dst = self.dst_input.text().strip()

        if not src or not dst:
            speak("Source and destination required")
            return

        try:
            os.rename(src, dst)
            speak("File renamed successfully")
            self.controller.log(f"Renamed {src} → {dst}")
            QTimer.singleShot(1000, self.close)
        except Exception as e:
            self.controller.log(str(e))
            speak("Rename failed")
        
        speak("Please Check the output sir.")

class MakeZipWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Make A Zip File")
        self.resize(300, 150)

        self.src_input = LoggedLineEdit()
        self.dst_input = LoggedLineEdit()

        self.btn = QPushButton("Make A Zip")
        self.btn.clicked.connect(self.zip_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Source file"))
        layout.addWidget(self.src_input)
        layout.addWidget(QLabel("Destination file"))
        layout.addWidget(self.dst_input)
        layout.addWidget(self.btn)

    def zip_file(self):
        src = self.src_input.text().strip()
        dst = self.dst_input.text().strip()

        if not src or not dst:
            speak("Source and destination required")
            return

        speak("Making Zip File")

        command = (f"Compress-Archive -Path \"{src}\" -DestinationPath \"{dst}\"")
        self.start_process("powershell",["-Command", command])

        speak("Please Check the output sir.")

class TypeWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("View File Content")
        self.resize(400, 100)

        self.input = LoggedLineEdit()
        self.btn = QPushButton("View")
        self.btn.clicked.connect(self.type_file)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("File path"))
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def type_file(self):
        path = self.input.text().strip()

        if not path:
            speak("File path required")
            return

        self.start_process("cmd", ["/c", "type", path])
        speak("Please Check the output sir.")

class TreeWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Display the tree of a directory")
        self.resize(400, 100)

        speak("The window has been popped up, please enter the information sir.")

        self.label = QLabel("Enter Directory")
        self.input = LoggedLineEdit()
        self.input.setPlaceholderText("Leave empty for current directory")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.tree_file)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)
        self.process.finished.connect(self.on_finished)

    def tree_file(self):
        path = self.input.text().strip() or "."
        self.label.setText("Running...")
        self.process.start("cmd", ["/c", "tree", "/A", path])
        speak("Please Check the output sir.")

    def read_output(self):
        output = bytes(self.process.readAllStandardOutput()).decode(
            "cp1252", errors="replace"
        )
        self.controller.log(output)

    def read_error(self):
        error = bytes(self.process.readAllStandardError()).decode(
            "cp1252", errors="replace"
        )
        self.controller.log(f"ERROR: {error}")

    def on_finished(self):
        self.label.setText("Done")
        QTimer.singleShot(1200, self.close)
