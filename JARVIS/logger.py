import logging
import sys

# Création du logger principal
logger = logging.getLogger("JARVIS")
logger.setLevel(logging.INFO)  # Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Format du message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler pour afficher dans la console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Handler pour écrire dans un fichier (mode append)
file_handler = logging.FileHandler("jarvis.log", encoding='utf-8')
file_handler.setFormatter(formatter)

# Ajout des handlers au logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
