import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from core.context_manager import ContextManager
from core.agenda_manager import AgendaManager
from core.news_manager import NewsManager
from core.media_controller import MediaController
from config import Config

logger = logging.getLogger(__name__)

class AIProcessor:
    """Gestionnaire de génération de texte via modèle Hugging Face local"""

    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.context_manager = ContextManager()
        self.agenda_manager = AgendaManager()
        self.news_manager = NewsManager()
        self.media_controller = MediaController()
        self.load_model()

    def load_model(self):
        """Charge le modèle et le tokenizer depuis le dossier local"""
        try:
            logger.info("Chargement modèle IA...")
            self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME, local_files_only=True)
            self.model = AutoModelForCausalLM.from_pretrained(Config.MODEL_NAME, local_files_only=True)

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            logger.info("Modèle chargé avec succès.")
        except Exception as e:
            logger.error(f"Erreur chargement modèle: {e}")

    def create_prompt(self, user_input: str) -> str:
        """Crée un prompt enrichi pour le modèle"""
        history = self.context_manager.get_context_for_ai()

        prompt = f"""Tu es J.A.R.V.I.S., un assistant personnel intelligent et poli.
RÈGLES IMPORTANTES :
- Tu t'adresses TOUJOURS à l'utilisateur en l'appelant "monsieur".
- Tes réponses sont courtes, claires, utiles et polies.
- Tu parles exclusivement en français.
- Tu évites toute répétition ou absurdité.

Contexte :
{history}

Utilisateur : {user_input}
J.A.R.V.I.S. :"""
        return prompt

    def generate_response(self, user_input: str) -> str:
        """Génère une réponse en se basant sur le prompt utilisateur"""
        try:
            prompt = self.create_prompt(user_input)
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(self.model.device)

            output = self.model.generate(
                **inputs,
                max_new_tokens=Config.MAX_TOKEN_LENGTH,
                temperature=Config.TEMPERATURE,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                top_k=50,
                top_p=0.95
            )

            full_output = self.tokenizer.decode(output[0], skip_special_tokens=True)
            response = full_output.split("J.A.R.V.I.S.:")[-1].strip()

            # Sauvegarde du contexte
            self.context_manager.add_to_history(user_input, response)

            return response
        except Exception as e:
            logger.error(f"Erreur génération réponse IA: {e}")
            return "Désolé monsieur, une erreur est survenue lors du traitement de votre demande."
