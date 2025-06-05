"""
test_fileio.py

📄 Teste les fonctions d'entrée/sortie de fichiers :
- Lecture et écriture de fichiers CSV
- Gestion des erreurs lors de l’ouverture de fichiers
- Intégration avec le système de logger global

🎯 Ces tests garantissent que les modules de sauvegarde et de chargement
fonctionnent correctement avec des données simulées.
"""

import os
import tempfile
import pytest
from utils import fileio
from utils import logger


class TestFileIO:

    def test_write_and_read_csv(self):
        """🧪 Vérifie l’écriture et lecture d’un fichier CSV temporaire."""
        data = [["année", "valeur"], [2025, 1000], [2026, 1200]]

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test_data.csv")

            # Écriture
            fileio.write_csv(file_path, data)
            assert os.path.exists(file_path), "❌ Fichier CSV non créé"

            # Lecture
            result = fileio.read_csv(file_path)
            expected = [['année', 'valeur'], ['2025', '1000'], ['2026', '1200']]
            assert result == expected, f"❌ Contenu incorrect : {result}"

    def test_logger_usage_during_io(self, caplog):
        """🧪 Vérifie que le logger global est utilisé pendant les I/O."""
        log = logger.get_logger("test_fileio")

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "log_test.csv")
            data = [["col1", "col2"], ["A", "B"]]

            with caplog.at_level("INFO"):
                fileio.write_csv(file_path, data)

        assert any("Écriture dans le fichier" in r.message for r in caplog.records), \
            "❌ Aucun log trouvé pendant l’écriture"

    def test_read_nonexistent_file_raises(self):
        """⚠️ Vérifie qu’une erreur est levée si le fichier CSV est introuvable."""
        with pytest.raises(FileNotFoundError, match=".*nonexistent_file.csv.*"):
            fileio.read_csv("nonexistent_file.csv")

    def test_write_invalid_path_raises(self):
        """⚠️ Vérifie qu’une erreur est levée si le chemin est invalide."""
        with pytest.raises(Exception):
            fileio.write_csv("/invalid/path/test.csv", [["x"]])
