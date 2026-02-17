from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QFileDialog
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
import webbrowser
import os

class LocalHTMLLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open Local HTML File")
        self.resize(450, 200)

        self.run_btn = QPushButton("Select HTML File")
        self.status_label = QLabel("Status: Idle")

        self.run_btn.clicked.connect(self.open_html_file)

        layout = QVBoxLayout(self)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def open_html_file(self):
        html_file, _ = QFileDialog.getOpenFileName(self, "Select HTML File", filter="HTML Files (*.html *.htm)")
        if not html_file:
            self.status_label.setText("Status: No file selected")
            speak("No HTML file selected")
            return

        try:
            html_path = f"file:///{os.path.abspath(html_file)}"
            webbrowser.open(html_path, new=2)  # Open in new tab
            self.status_label.setText("Status: HTML file opened successfully")
            speak("HTML file opened successfully")
            
        except Exception as e:
            self.status_label.setText("Status: Failed to open HTML file")
            speak("Failed to open HTML file")
            print("Error:", e)
