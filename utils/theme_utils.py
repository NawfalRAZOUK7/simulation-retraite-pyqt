# utils/theme_utils.py

import os
import json
import logging
from ui.dialogs import show_error, show_warning

DEFAULT_CONFIG_PATH = "data/config/ui_prefs.json"
logger = logging.getLogger("ui.theme_utils")

def ensure_config_dir_exists():
    """Crée le dossier config si absent."""
    try:
        os.makedirs(os.path.dirname(DEFAULT_CONFIG_PATH), exist_ok=True)
    except Exception as e:
        logger.error(f"[theme_utils] Impossible de créer le dossier config : {e}")

def load_prefs(config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Charge tout le dict de prefs UI, ou crée un dict vide si absent/corrompu."""
    if not os.path.exists(config_path):
        logger.info(f"[theme_utils] Fichier de config absent ({config_path}), valeurs par défaut.")
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            prefs = json.load(f)
        if not isinstance(prefs, dict):
            raise ValueError("Format non dict")
        return prefs
    except Exception as e:
        logger.warning(f"[theme_utils] Erreur lors du chargement prefs ({e}) — reset fichier.")
        if parent:
            show_warning(f"Erreur de lecture des préférences UI.\nRéinitialisation du fichier.\n\n{e}", parent)
        reset_theme_pref(config_path, parent)
        return {}

def save_prefs(prefs, config_path=DEFAULT_CONFIG_PATH, parent=None):
    ensure_config_dir_exists()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)
        logger.info(f"[theme_utils] Préférences UI sauvegardées dans {config_path}")
        return True
    except Exception as e:
        logger.error(f"[theme_utils] Erreur lors de la sauvegarde des prefs : {e}")
        if parent:
            show_error(f"Impossible de sauvegarder les préférences UI.\n\n{e}", parent)
        return False

def save_theme_pref(dark_mode, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Sauvegarde la clé dark_mode (True/False) dans le fichier prefs."""
    prefs = load_prefs(config_path, parent)
    prefs["dark_mode"] = bool(dark_mode)
    return save_prefs(prefs, config_path, parent)

def load_theme_pref(config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Charge la clé dark_mode (True/False), default=False."""
    prefs = load_prefs(config_path, parent)
    return bool(prefs.get("dark_mode", False))

def save_ui_pref(key, value, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Sauvegarde une préférence générique UI."""
    prefs = load_prefs(config_path, parent)
    prefs[key] = value
    return save_prefs(prefs, config_path, parent)

def load_ui_pref(key, default=None, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Charge une préférence UI générique."""
    prefs = load_prefs(config_path, parent)
    return prefs.get(key, default)

def reset_theme_pref(config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Supprime la config pour repartir sur la valeur par défaut."""
    try:
        if os.path.exists(config_path):
            os.remove(config_path)
            logger.info(f"[theme_utils] Préférences UI réinitialisées ({config_path})")
            return True
        return False
    except Exception as e:
        logger.error(f"[theme_utils] Erreur lors de la suppression de la config thème : {e}")
        if parent:
            show_error(f"Impossible de supprimer le fichier de préférences UI.\n\n{e}", parent)
        return False

# --- Exemple d'utilisation ---
"""
from utils.theme_utils import save_theme_pref, load_theme_pref

# Pour sauver avec feedback (dans une fenêtre) :
save_theme_pref(True, parent=self)
is_dark = load_theme_pref(parent=self)
"""
