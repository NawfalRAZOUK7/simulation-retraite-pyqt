"""
test_structure.py

Vérifie l’architecture de base du projet :
- Présence des dossiers data/config/ et data/output/
- Capacité à écrire et supprimer un fichier dans ces dossiers
- Présence des modules principaux (core/, ui/, utils/)
- Importabilité des composants critiques (logger, theme, widgets…)

Ce test garantit que le projet démarre sans bug d’environnement,
et que les exports/sauvegardes sont toujours possibles.
"""

import os
import sys
import importlib
import pytest

# Ajout du chemin racine du projet
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

# Dossiers attendus
REQUIRED_FOLDERS = [
    "data/config",
    "data/output",
]

# Modules critiques à importer
CRITICAL_MODULES = [
    "core.simulator",
    "core.employee",
    "core.retiree",
    "core.scenario",
    "core.germes",

    "ui.main_window",
    "ui.menu_window",
    "ui.charts_window.charts_window",
    "ui.charts_window.tab_reserve",
    "ui.charts_window.tab_comparaison",
    "ui.charts_window.tab_confidence",
    "ui.charts_window.scenario_selector",

    "ui.widgets.animated_tool_button",
    "ui.widgets.fade_tab_widget",
    "ui.widgets.fade_widget",

    "ui.theme",
    "utils.theme_utils",
    "utils.fileio",
    "utils.stats",
    "utils.logger",
]


class TestProjectStructure:
    @pytest.mark.parametrize("folder", REQUIRED_FOLDERS)
    def test_required_folders_exist(self, folder):
        """Vérifie que les dossiers requis existent."""
        path = os.path.join(BASE_PATH, folder)
        assert os.path.isdir(path), f"Dossier manquant : {folder}"

    @pytest.mark.parametrize("folder", REQUIRED_FOLDERS)
    def test_file_write_delete_in_folder(self, folder):
        """Vérifie la capacité à écrire et supprimer un fichier dans le dossier donné."""
        path = os.path.join(BASE_PATH, folder)
        test_file = os.path.join(path, "test_temp_file.txt")
        try:
            with open(test_file, "w") as f:
                f.write("test")
            assert os.path.isfile(test_file)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    @pytest.mark.parametrize("module_path", CRITICAL_MODULES)
    def test_critical_module_imports(self, module_path):
        """Teste que les modules essentiels peuvent être importés sans erreur."""
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            pytest.fail(f"Échec d’import : {module_path} — {e}")

    def test_logger_structure(self):
        """Teste la présence et la structure du logger principal."""
        from utils import logger
        log = logger.get_logger("test_structure")
        assert log.name == "test_structure"
        log.info("Test de logger OK.")

    def test_theme_utils_available(self):
        """Teste la présence des fonctions utilitaires de thème."""
        from ui import theme
        from utils import theme_utils

        assert hasattr(theme, "dark_palette")
        assert hasattr(theme, "light_palette")
        assert hasattr(theme_utils, "load_theme_preference")
        assert hasattr(theme_utils, "save_theme_preference")
