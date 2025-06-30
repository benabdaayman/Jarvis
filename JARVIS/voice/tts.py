import pyttsx3
from PyQt6.QtCore import QThread, pyqtSignal
import logging

logger = logging.getLogger(__name__)

class TTSThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.engine = pyttsx3.init()
        
        # Config voix FR si disponible
        self.set_french_voice()
    
    def set_french_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "fr" in voice.languages or "French" in voice.name:
                self.engine.setProperty('voice', voice.id)
                logger.info(f"Voix française sélectionnée: {voice.name}")
                break
    
    def run(self):
        try:
            logger.info(f"Synthèse vocale démarrée: {self.text}")
            self.engine.say(self.text)
            self.engine.runAndWait()
            self.finished.emit()
            logger.info("Synthèse vocale terminée")
        except Exception as e:
            logger.error(f"Erreur synthèse vocale: {e}")
            self.error.emit(str(e))
