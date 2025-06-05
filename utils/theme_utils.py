import os
import json

# Logger central
try:
    from utils.logger import get_child_logger
    logger = get_child_logger("ui.theme_utils")
except ImportError:
    import logging
    logger = logging.getLogger("ui.theme_utils")

# UI feedback dialogs
from ui.dialogs import show_error, show_warning

DEFAULT_CONFIG_PATH = "data/config/ui_prefs.json"

def ensure_config_dir_exists():
    """Crée le dossier contenant le fichier de configuration si nécessaire."""
    try:
        os.makedirs(os.path.dirname(DEFAULT_CONFIG_PATH), exist_ok=True)
    except Exception as e:
        logger.error("Impossible de créer le dossier config : %s", e)

def load_prefs(config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Charge le dictionnaire des préférences UI, ou renvoie un dict vide si absent/corrompu."""
    if not os.path.exists(config_path):
        logger.info("Fichier de config absent (%s), valeurs par défaut utilisées.", config_path)
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            prefs = json.load(f)
        if not isinstance(prefs, dict):
            raise ValueError("Le contenu du fichier n'est pas un dictionnaire.")
        return prefs
    except Exception as e:
        logger.warning("Erreur lors du chargement des préférences (%s) — réinitialisation.", e)
        if parent:
            show_warning(f"Erreur de lecture des préférences UI.\nFichier réinitialisé.\n\n{e}", parent)
        reset_theme_pref(config_path, parent)
        return {}

def save_prefs(prefs, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Sauvegarde le dictionnaire de préférences UI dans un fichier JSON."""
    ensure_config_dir_exists()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)
        logger.info("Préférences UI sauvegardées dans %s", config_path)
        return True
    except Exception as e:
        logger.error("Erreur lors de la sauvegarde des préférences : %s", e)
        if parent:
            show_error(f"Impossible de sauvegarder les préférences UI.\n\n{e}", parent)
        return False

def save_theme_pref(dark_mode, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Sauvegarde la préférence du mode sombre (True/False)."""
    prefs = load_prefs(config_path, parent)
    prefs["dark_mode"] = bool(dark_mode)
    return save_prefs(prefs, config_path, parent)

def load_theme_pref(config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Charge la préférence de mode sombre (par défaut False)."""
    prefs = load_prefs(config_path, parent)
    return bool(prefs.get("dark_mode", False))

def save_ui_pref(key, value, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Sauvegarde une préférence UI générique."""
    prefs = load_prefs(config_path, parent)
    prefs[key] = value
    return save_prefs(prefs, config_path, parent)

def load_ui_pref(key, default=None, config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Charge une préférence UI générique."""
    prefs = load_prefs(config_path, parent)
    return prefs.get(key, default)

def reset_theme_pref(config_path=DEFAULT_CONFIG_PATH, parent=None):
    """Supprime le fichier de préférences pour forcer un reset."""
    try:
        if os.path.exists(config_path):
            os.remove(config_path)
            logger.info("Fichier de préférences UI réinitialisé (%s)", config_path)
            return True
        return False
    except Exception as e:
        logger.error("Erreur lors de la suppression du fichier de préférences : %s", e)
        if parent:
            show_error(f"Impossible de supprimer le fichier de préférences UI.\n\n{e}", parent)
        return False

# --- Exemples d'utilisation ---
"""
from utils.theme_utils import save_theme_pref, load_theme_pref

# Pour sauver avec feedback dans un QWidget:
save_theme_pref(True, parent=self)
is_dark = load_theme_pref(parent=self)
"""

__all__ = [
    "load_prefs", "save_prefs", "save_theme_pref", "load_theme_pref",
    "save_ui_pref", "load_ui_pref", "reset_theme_pref", "ensure_config_dir_exists"
]
