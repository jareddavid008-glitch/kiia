from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QFileDialog
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
import os

class FolderLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open Folder")
        self.resize(450, 180)

        self.run_folder_btn = QPushButton("Open Folder")
        self.status_label = QLabel("Status: Idle")

        self.run_folder_btn.clicked.connect(self.open_folder)

        layout = QVBoxLayout(self)
        layout.addWidget(self.run_folder_btn)
        layout.addWidget(self.status_label)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            self.status_label.setText("Status: No folder selected")
            speak("No folder selected")
            return

        try:
            os.startfile(folder)
            self.status_label.setText("Status: Folder opened successfully")
            speak("Folder opened successfully")
        except Exception as e:
            self.status_label.setText("Status: Failed to open folder")
            speak("Failed to open folder")
            print("Error:", e)
