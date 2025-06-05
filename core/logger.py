# core/logger.py

"""
Fichier centralisé pour le logger du package `core`.
Permet d’éviter les imports circulaires tout en gardant un logger propre à `core`.
À utiliser dans tous les modules du dossier `core/` via :

    from core.logger import logger
"""

try:
    from utils.logger import get_child_logger
    logger = get_child_logger("core")
except ImportError:
    import logging
    logger = logging.getLogger("app.core")

logger.debug("Logger initialisé pour le module 'core'.")
