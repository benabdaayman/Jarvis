import os

class Config:
    """Configuration centralisée de l'application"""

    # Chemin absolu vers le dossier du projet (adapté Windows)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Modèles et paramètres IA
    # IMPORTANT : mettre le chemin complet vers le modèle local HF
    MODEL_NAME = os.path.join(BASE_DIR, "models", "local_hf_model")
    MAX_TOKEN_LENGTH = 100
    TEMPERATURE = 0.7

    # Audio
    SAMPLE_RATE = 16000
    DEVICE = None

    # API News (utilise une API gratuite)
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
    NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # À remplacer par ta clé
    NEWS_COUNTRY = "fr"

    # Interface
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    THEME_COLOR = "#2C3E50"
    ACCENT_COLOR = "#3498DB"

    # Fichiers de données
    AGENDA_FILE = os.path.join(BASE_DIR, "data", "agenda.json")
    CONTEXT_FILE = os.path.join(BASE_DIR, "data", "context.json")

    # VOSK model path
    VOSK_MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-fr-0.22")
