import json
import os
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class ContextManager:
    """Gère l'historique de conversation et les préférences de session"""

    def __init__(self):
        self.context = {
            "user_name": "monsieur",
            "conversation_history": [],
            "preferences": {},
            "session_start": datetime.now().isoformat()
        }
        self.load_context()

    def load_context(self):
        """Charge le contexte depuis un fichier JSON"""
        try:
            if os.path.exists(Config.CONTEXT_FILE):
                with open(Config.CONTEXT_FILE, 'r', encoding='utf-8') as f:
                    self.context.update(json.load(f))
            else:
                self.save_context()
        except Exception as e:
            logger.error(f"Erreur chargement contexte: {e}")

    def save_context(self):
        """Sauvegarde le contexte dans un fichier JSON"""
        try:
            with open(Config.CONTEXT_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.context, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde contexte: {e}")

    def add_to_history(self, user_input: str, ai_response: str):
        """Ajoute un échange à l'historique et limite à 10 entrées"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "ai": ai_response
        }
        self.context["conversation_history"].append(entry)
        self.context["conversation_history"] = self.context["conversation_history"][-10:]
        self.save_context()

    def get_context_for_ai(self) -> str:
        """Formate l'historique pour l'intégrer dans le prompt"""
        history = self.context.get("conversation_history", [])[-3:]
        formatted = ""
        for exchange in history:
            formatted += f"Utilisateur : {exchange['user']}\nJ.A.R.V.I.S. : {exchange['ai']}\n"
        return formatted
