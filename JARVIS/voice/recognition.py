# voice/recognition.py

import vosk
import sounddevice as sd
import queue
import json
from PyQt6.QtCore import QThread, pyqtSignal
from config import Config
import os

class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.q = queue.Queue()
        self.model = None
        self.stream = None
        self.running = True

    def run(self):
        try:
            if not self.model:
                model_path = Config.VOSK_MODEL_PATH
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Modèle VOSK introuvable à {model_path}")
                self.model = vosk.Model(model_path)

            self.stream = sd.RawInputStream(samplerate=Config.SAMPLE_RATE,
                                            blocksize=8000,
                                            dtype='int16',
                                            channels=1,
                                            callback=self.callback)
            self.stream.start()

            rec = vosk.KaldiRecognizer(self.model, Config.SAMPLE_RATE)

            while self.running:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        self.recognized_text.emit(text)

        except Exception as e:
            print(f"[ERREUR VOSK] {e}")

        finally:
            if self.stream:
                self.stream.stop()
                self.stream.close()

    def callback(self, indata, frames, time, status):
        if status:
            print(f"Statut microphone: {status}")
        self.q.put(bytes(indata))

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
