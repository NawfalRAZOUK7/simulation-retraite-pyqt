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
import importlib
import pytest

# Dossiers attendus relatifs au projet
REQUIRED_FOLDERS = [
    "data/config",
    "data/output",
]

# Modules essentiels à importer (sans ui.main_window)
CRITICAL_MODULES = [
    "core.simulator",
    "core.employee",
    "core.retiree",
    "core.scenario",
    "core.germes",

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
        """Vérifie que les dossiers requis existent dans le projet."""
        assert os.path.isdir(folder), f"❌ Dossier requis manquant : {folder}"

    @pytest.mark.parametrize("folder", REQUIRED_FOLDERS)
    def test_file_write_delete_in_folder(self, folder):
        """Teste la possibilité d’écrire et de supprimer un fichier dans les dossiers projet."""
        test_file = os.path.join(folder, "test_temp_file.txt")
        try:
            with open(test_file, "w") as f:
                f.write("test")
            assert os.path.isfile(test_file), f"❌ Écriture échouée dans : {folder}"
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    @pytest.mark.parametrize("module_path", CRITICAL_MODULES)
    def test_critical_module_imports(self, module_path):
        """Teste que tous les modules critiques peuvent être importés sans erreur."""
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            pytest.fail(f"❌ Erreur d’import : {module_path} → {e}")

    def test_logger_structure(self):
        """Teste la structure du logger global."""
        from utils import logger
        log = logger.get_logger("test_structure")
        assert log.name.endswith("test_structure"), f"❌ Nom inattendu : {log.name}"
        log.info("✅ Logger importé et fonctionnel")

    def test_theme_utils_available(self):
        """Vérifie la présence des fonctions pour thèmes et préférences utilisateur."""
        from ui import theme
        from utils import theme_utils

        assert hasattr(theme, "get_dark_palette"), "❌ get_dark_palette() manquant"
        assert hasattr(theme, "get_light_palette"), "❌ get_light_palette() manquant"
        assert hasattr(theme_utils, "load_theme_pref"), "❌ load_theme_pref() manquant"
        assert hasattr(theme_utils, "save_theme_pref"), "❌ save_theme_pref() manquant"
