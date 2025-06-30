import sys
import logging

from PyQt6.QtWidgets import QApplication

from ui.main_window import JarvisMainWindow
from core.context_manager import ContextManager

# Configuration du logger global
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jarvis.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Démarrage de J.A.R.V.I.S.")
    
    app = QApplication(sys.argv)
    
    # Charger ou initialiser le contexte global
    context_manager = ContextManager()
    
    window = JarvisMainWindow()
    window.show()
    
    exit_code = app.exec()
    
    # Sauvegarder contexte à la fermeture
    context_manager.save_context()
    
    logger.info("Fermeture de J.A.R.V.I.S.")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
