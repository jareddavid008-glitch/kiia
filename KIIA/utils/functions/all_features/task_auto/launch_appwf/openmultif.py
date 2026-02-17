from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QFileDialog
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
import os

class MultiFileLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open Multiple Files")
        self.resize(450, 200)

        self.run_btn = QPushButton("Select and Open Multiple Files")
        self.status_label = QLabel("Status: Idle")

        self.run_btn.clicked.connect(self.open_multiple_files)

        layout = QVBoxLayout(self)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def open_multiple_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select files to open")
        if not files:
            self.status_label.setText("Status: No files selected")
            speak("No files selected")
            return

        success_count = 0
        for f in files:
            try:
                os.startfile(f)
                success_count += 1
            except Exception as e:
                print(f"Failed to open {f}: {e}")

        self.status_label.setText(f"Status: Opened {success_count} files")
        speak(f"Opened {success_count} files successfully")
