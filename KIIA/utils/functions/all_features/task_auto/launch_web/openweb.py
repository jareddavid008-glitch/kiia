from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
from .....tools.logger import LoggedLineEdit
import webbrowser

class DefaultBrowserLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open URL in Default Browser")
        self.resize(450, 180)

        self.url_input = LoggedLineEdit()
        self.run_btn = QPushButton("Open URL")
        self.status_label = QLabel("Status: Idle")

        self.url_input.textChanged.connect(lambda text: self.run_btn.setEnabled(bool(text.strip())))
        self.run_btn.clicked.connect(self.open_url)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def open_url(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Status: No URL provided")
            speak("Please provide a URL")
            return

        try:
            webbrowser.open(url, new=2)
            self.status_label.setText("Status: URL opened in default browser")
            speak("URL opened successfully")
        except Exception as e:
            self.status_label.setText("Status: Failed to open URL")
            speak("Failed to open URL")
            print("Error:", e)
