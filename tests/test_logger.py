"""
test_logger.py

Teste le module global de logging :
- Vérifie que le logger principal est bien accessible
- Vérifie les niveaux de logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Vérifie la création du fichier de logs si activé
- Vérifie que les loggers enfants héritent bien de la configuration globale

Ce test garantit que tous les modules du projet peuvent journaliser de manière cohérente,
et que les fichiers de log sont générés de manière fiable.
"""

import os
import tempfile
import logging
import pytest
from utils import logger


class TestLogger:
    def test_get_logger_returns_logger_instance(self):
        """Teste que get_logger() retourne une instance valide."""
        log = logger.get_logger("test_logger")
        assert isinstance(log, logging.Logger)
        assert log.name == "test_logger"

    def test_logger_levels(self, caplog):
        """Teste que les différents niveaux de logs fonctionnent correctement."""
        log = logger.get_logger("test_logger_levels")
        with caplog.at_level(logging.DEBUG):
            log.debug("Debug msg")
            log.info("Info msg")
            log.warning("Warn msg")
            log.error("Error msg")
            log.critical("Critical msg")

        levels = ["Debug msg", "Info msg", "Warn msg", "Error msg", "Critical msg"]
        for message in levels:
            assert any(message in record.message for record in caplog.records)

    def test_logger_file_output(self):
        """Teste que le logger peut écrire dans un fichier temporaire."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test_log_output.log")

            # Créer un handler temporaire
            log = logger.get_logger("file_output_test")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            log.addHandler(file_handler)

            # Logger un message
            log.info("Test log message to file.")

            # Fermer et retirer handler
            log.removeHandler(file_handler)
            file_handler.close()

            # Lire fichier
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Test log message to file." in content

    def test_child_logger_inherits_config(self, caplog):
        """Teste que les loggers enfants héritent des paramètres du logger principal."""
        parent_log = logger.get_logger("parent")
        child_log = logger.get_logger("parent.child")

        with caplog.at_level(logging.INFO):
            child_log.info("Child logger message")

        assert "Child logger message" in caplog.text
