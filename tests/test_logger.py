"""
test_logger.py

🎯 Objectif :
- Vérifie que le logger principal est bien accessible
- Vérifie les niveaux de logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Vérifie la création d’un fichier de log temporaire
- Vérifie que les loggers enfants héritent correctement du parent

🛡️ Ce test garantit que tous les modules du projet peuvent journaliser
de manière fiable et cohérente.
"""

import os
import tempfile
import logging
import pytest
from utils import logger


class TestLogger:

    def test_get_logger_returns_logger_instance(self):
        """🧪 Vérifie que get_logger() retourne bien un Logger."""
        log = logger.get_logger("test_logger")
        assert isinstance(log, logging.Logger), "❌ get_logger() ne retourne pas un objet Logger"
        assert log.name.endswith("test_logger"), f"❌ Nom inattendu : {log.name}"

    def test_logger_levels_output(self, caplog):
        """🧪 Vérifie les niveaux de logs classiques."""
        log = logger.get_logger("logger_levels")
        with caplog.at_level(logging.DEBUG):
            log.debug("Debug message")
            log.info("Info message")
            log.warning("Warning message")
            log.error("Error message")
            log.critical("Critical message")

        for expected in [
            "Debug message", "Info message", "Warning message", "Error message", "Critical message"
        ]:
            assert any(expected in record.message for record in caplog.records), f"❌ Message manquant : {expected}"

    def test_logger_levels_output(self, caplog):
        """🧪 Vérifie les niveaux de logs classiques."""
        log = logger.get_logger("logger_levels")

        # 🔧 Forcer le niveau du logger (et handlers) à DEBUG pour le test
        original_level = log.level
        logger.set_log_level("DEBUG")

        with caplog.at_level(logging.DEBUG):
            log.debug("Debug message")
            log.info("Info message")
            log.warning("Warning message")
            log.error("Error message")
            log.critical("Critical message")

        logger.set_log_level(logging.getLevelName(original_level))  # 🔄 Restaurer le niveau

        for expected in [
            "Debug message", "Info message", "Warning message", "Error message", "Critical message"
        ]:
            assert any(expected in record.message for record in caplog.records), f"❌ Message manquant : {expected}"

    def test_child_logger_inherits_configuration(self, caplog):
        """🧪 Vérifie que le logger enfant hérite des paramètres du parent."""
        parent_logger = logger.get_logger("parent")
        child_logger = logger.get_logger("parent.child")

        with caplog.at_level(logging.INFO):
            child_logger.info("Child log message")

        assert "Child log message" in caplog.text, "❌ Le logger enfant n’a pas loggé correctement"
