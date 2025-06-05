# ui/charts_window/logger.py

"""
Fichier centralisé pour le logger du package `charts_window`.
Permet d’éviter les imports circulaires tout en gardant un logger propre à `charts_window`.
À utiliser dans tous les modules du dossier `charts_window/` via :

    from charts_window.logger import logger
"""


try:
    from utils.logger import get_child_logger
    logger = get_child_logger("ui.charts_window")
except ImportError:
    import logging
    logger = logging.getLogger("ui.charts_window")
