# csv_import_window/logger.py

"""
Fichier centralisé pour le logger du package `csv_import_window`.
Permet d’éviter les imports circulaires tout en gardant un logger propre à `csv_import_window`.
À utiliser dans tous les modules du dossier `csv_import_window/` via :

    from csv_import_window.logger import logger
"""

try:
    from utils.logger import get_child_logger
    logger = get_child_logger("csv_import_window")
except ImportError:
    import logging
    logger = logging.getLogger("app.csv_import_window")

logger.debug("Logger initialisé pour le module 'csv_import_window'.")
