import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class NewsManager:
    """Récupère les actualités via une API externe"""

    def __init__(self):
        self.api_key = Config.NEWS_API_KEY

    def get_top_news(self, max_articles: int = 5):
        """Renvoie une liste de titres d'actualités"""
        if self.api_key == "YOUR_NEWS_API_KEY":
            return [{"title": "Veuillez configurer une clé API valide dans Config.NEWS_API_KEY."}]
        
        try:
            response = requests.get(Config.NEWS_API_URL, params={
                "apiKey": self.api_key,
                "country": Config.NEWS_COUNTRY,
                "pageSize": max_articles
            }, timeout=10)
            response.raise_for_status()
            return response.json().get("articles", [])
        except Exception as e:
            logger.error(f"Erreur récupération news: {e}")
            return [{"title": "Impossible de récupérer les actualités pour le moment."}]
