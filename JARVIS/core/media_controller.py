import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

class MediaController:
    """Contrôle basique du média (play/pause, volume)"""

    @staticmethod
    def play_pause():
        try:
            if sys.platform == "win32":
                subprocess.run(["nircmd", "sendkeypress", "space"], check=False)
            elif sys.platform == "darwin":
                subprocess.run(["osascript", "-e", 'tell app "Music" to playpause'], check=False)
            else:
                subprocess.run(["playerctl", "play-pause"], check=False)
            return True
        except Exception as e:
            logger.error(f"Erreur play/pause média: {e}")
            return False

    @staticmethod
    def volume_up():
        try:
            if sys.platform == "win32":
                subprocess.run(["nircmd", "changesysvolume", "5000"], check=False)
            else:
                subprocess.run(["amixer", "sset", "Master", "5%+"], check=False)
            return True
        except Exception as e:
            logger.error(f"Erreur volume up: {e}")
            return False

    @staticmethod
    def volume_down():
        try:
            if sys.platform == "win32":
                subprocess.run(["nircmd", "changesysvolume", "-5000"], check=False)
            else:
                subprocess.run(["amixer", "sset", "Master", "5%-"], check=False)
            return True
        except Exception as e:
            logger.error(f"Erreur volume down: {e}")
            return False
