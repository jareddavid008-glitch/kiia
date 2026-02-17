from PyQt6.QtWidgets import (
    QWidget, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedLayout,
    QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor, QMovie
from PyQt6.QtCore import Qt
from datetime import datetime
from .all_features.task_auto.launch_app import openwargs
from utils.tools.logger import write_log
import socket
import json
import os

path = os.path.expandvars("C:/Users/%USERNAME%/OneDrive/Desktop/KIIA/KIIA_OUTPUT")
path_log = os.path.join(path, "KIIA_LOG.json")
LOG_FILE = path_log

class KIIAHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_label.setScaledContents(True)

        gif_path = os.path.expandvars(r"C:\Users\%USERNAME%\OneDrive\Desktop\KIIA\utils\assets\kiia.gif")
        self.movie = QMovie(gif_path)
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.gif_label)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(0, 160, 255, 90))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

# ================= Left Toolbar =================
class LeftToolBar(QWidget):
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl
        self.setFixedWidth(190)

        self.setStyleSheet("""
            QWidget {
                background: #0d1117;
                border-right: 1px solid rgba(0, 170, 255, 0.18);
            }
            QPushButton {
                background: #161b22;
                color: #c9d1d9;
                border: none;
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 13px;
                font-weight: 500;
                margin: 6px 12px;
                text-align: left;
            }
            QPushButton:hover {
                background: #21262d;
            }
            QPushButton:pressed {
                background: #30363d;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(6)
        layout.setContentsMargins(12, 30, 12, 20)

        buttons = [
            ("Main Menu", self.ctrl.show_main),
            ("Output", self.ctrl.show_output),
            ("Load Log", self.ctrl.show_log),
            ("Clear Output", self.ctrl.clear_output),
            ("OpenExeWithArgsWindow", self.ctrl.open_whoami),
        ]

        for text, slot in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

        layout.addStretch()
        
# ================= MAIN WINDOW =================
class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KIIA Control Panel")
        self.resize(940, 700)
        self.setStyleSheet("""
            QWidget {
                background: #0a0c12;
                color: #d0e0ff;
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
            }
            QLabel {
                color: #58a6ff;
            }
        """)

        status = QLabel("KIIA ONLINE")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            background: #0f1620;
            border-bottom: 1px solid rgba(0, 170, 255, 0.15);
            padding: 14px 0;
        """)

        self.toolbar = LeftToolBar(self)
        self.hud = KIIAHUD()

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background: #0d1117;
                color: #c9d1d9;
                border: 1px solid rgba(0, 170, 255, 0.20);
                border-radius: 8px;
                padding: 14px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
            }
        """)

        self.page_main = QWidget()
        m = QVBoxLayout(self.page_main)
        m.setContentsMargins(50, 30, 50, 50)
        m.addStretch(1)
        m.addWidget(self.hud, 0, Qt.AlignmentFlag.AlignCenter)
        m.addStretch(1)

        self.page_output = QWidget()
        o = QVBoxLayout(self.page_output)
        o.setContentsMargins(30, 30, 30, 30)
        o.addWidget(self.output)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.page_main)
        self.stack.addWidget(self.page_output)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self.toolbar)
        body.addLayout(self.stack, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(status)
        layout.addLayout(body)

        # Bottom status - very subtle
        bottom = QLabel(f"HOSTNAME: {socket.gethostname()}")
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom.setStyleSheet("""
            font-size: 12px;
            color: #6e7681;
            background: #0f1620;
            padding: 10px;
            border-top: 1px solid rgba(0, 170, 255, 0.12);
        """)
        layout.addWidget(bottom)

        self.log("KIIA ONLINE - System ready")

    def log(self, text):
        self.output.append(f"> {text}")
        write_log("KIIA", text)

    def show_main(self):
        self.stack.setCurrentIndex(0)

    def show_output(self):
        self.stack.setCurrentIndex(1)
    
    def show_log(self):
        self.stack.setCurrentIndex(1) 

        if not os.path.exists(LOG_FILE):
            self.output.setPlainText("Log file not found.")
            return

        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
            conversation = ""
            for entry in logs:
                ts = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                conversation += f"[{ts}] {entry['sender']}: {entry['message']}\n"

            self.output.clear()
            self.output.setPlainText(conversation)

        except json.JSONDecodeError:
            self.output.setPlainText("Log file is corrupted.")

    def clear_output(self):
        self.output.clear()
        
    def open_whoami(self):
        self.open_tree_win = openwargs.OpenExeWithArgsWindow(self)
        self.open_tree_win.show()
