# results_window/logger.py

"""
Fichier centralisé pour le logger du package `results_window`.
Permet d’éviter les imports circulaires tout en gardant un logger propre à `results_window`.
À utiliser dans tous les modules du dossier `results_window/` via :

    from results_window.logger import logger
"""

try:
    from utils.logger import get_child_logger
    logger = get_child_logger("results_window")
except ImportError:
    import logging
    logger = logging.getLogger("app.results_window")

logger.debug("Logger initialisé pour le module 'core'.")
