import json
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from config import Config

logger = logging.getLogger(__name__)

class AgendaManager:
    """Gère l'ajout, la suppression et la récupération d'événements"""

    def __init__(self):
        self.agenda = []
        self.load_agenda()

    def load_agenda(self):
        """Charge l'agenda depuis un fichier JSON"""
        try:
            if os.path.exists(Config.AGENDA_FILE):
                with open(Config.AGENDA_FILE, 'r', encoding='utf-8') as f:
                    self.agenda = json.load(f)
            else:
                self.save_agenda()
        except Exception as e:
            logger.error(f"Erreur chargement agenda: {e}")

    def save_agenda(self):
        """Sauvegarde l'agenda"""
        try:
            with open(Config.AGENDA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.agenda, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde agenda: {e}")

    def add_event(self, title: str, date_str: str, time_str: str = "09:00") -> bool:
        """Ajoute un nouvel événement"""
        try:
            event_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            self.agenda.append({
                "id": len(self.agenda) + 1,
                "title": title,
                "datetime": event_datetime.isoformat(),
                "created": datetime.now().isoformat()
            })
            self.save_agenda()
            return True
        except Exception as e:
            logger.error(f"Erreur ajout événement: {e}")
            return False

    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Retourne les événements dans les x prochains jours"""
        now = datetime.now()
        future = now + timedelta(days=days)
        return sorted(
            [event for event in self.agenda if now <= datetime.fromisoformat(event["datetime"]) <= future],
            key=lambda e: e["datetime"]
        )

    def remove_event(self, event_id: int) -> bool:
        """Supprime un événement par son ID"""
        try:
            self.agenda = [e for e in self.agenda if e["id"] != event_id]
            self.save_agenda()
            return True
        except Exception as e:
            logger.error(f"Erreur suppression événement: {e}")
            return False
