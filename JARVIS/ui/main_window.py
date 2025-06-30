import sys
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QFrame, QApplication, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

from voice.recognition import SpeechRecognitionThread
from voice.tts import TTSThread
from core.ai_processor import AIProcessor
from ui.styles import STYLE

logger = logging.getLogger(__name__)

class JarvisMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("J.A.R.V.I.S.")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("ui/icons/jarvis_icon.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setStyleSheet("background-color:#34495E; color:#ecf0f1;")
        self.layout.addWidget(self.conversation_display)

        self.input_layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)

        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("background-color:#2C3E50; color:#ecf0f1;")
        self.input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Envoyer")
        self.send_button.setStyleSheet("background-color:#3498DB; color:white;")
        self.input_layout.addWidget(self.send_button)

        self.send_button.clicked.connect(self.handle_send)

        # Initialisation des threads
        self.speech_thread = SpeechRecognitionThread()
        self.tts_thread = None  # sera créé à la volée

        self.ai_processor = AIProcessor()

        # Connecter signal de reconnaissance vocale
        self.speech_thread.recognized_text.connect(self.handle_recognized_text)
        self.speech_thread.start()

        # Appliquer le style
        self.setStyleSheet(STYLE)

        # Message de bienvenue
        welcome_msg = "Bonjour monsieur, comment puis-je vous aider aujourd'hui ?"
        self.add_to_conversation("J.A.R.V.I.S.", welcome_msg)
        self.speak(welcome_msg)

    def add_to_conversation(self, speaker: str, text: str):
        self.conversation_display.append(f"<b>{speaker}:</b> {text}")

    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return
        self.add_to_conversation("Vous", user_text)
        self.input_field.clear()

        # Processer la requête IA en thread séparé si besoin
        response = self.ai_processor.generate_response(user_text)
        self.add_to_conversation("J.A.R.V.I.S.", response)
        self.speak(response)

    def handle_recognized_text(self, text: str):
        if text.strip() == "":
            return
        self.add_to_conversation("Vous (vocal)", text)
        response = self.ai_processor.generate_response(text)
        self.add_to_conversation("J.A.R.V.I.S.", response)
        self.speak(response)

    def speak(self, text: str):
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.terminate()
            self.tts_thread.wait()
        self.tts_thread = TTSThread(text)
        self.tts_thread.start()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Quitter', 'Voulez-vous vraiment quitter J.A.R.V.I.S. ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.speech_thread.isRunning():
                self.speech_thread.terminate()
                self.speech_thread.wait()
            if self.tts_thread and self.tts_thread.isRunning():
                self.tts_thread.terminate()
                self.tts_thread.wait()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisMainWindow()
    window.show()
    sys.exit(app.exec())
