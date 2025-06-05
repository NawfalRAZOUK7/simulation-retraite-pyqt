"""
test_theme.py

🎨 Teste les composants de gestion du thème :
- Génération des palettes claire et sombre (module ui.theme)
- Sauvegarde et chargement des préférences utilisateur (module utils.theme_utils)

🧪 Ces tests garantissent que le thème peut être appliqué, sauvegardé,
et restauré correctement entre les sessions utilisateur.
"""

import os
import tempfile
import pytest
from PyQt5.QtGui import QPalette
from ui import theme
from utils import theme_utils


class TestThemePalettes:

    def test_dark_palette_is_valid(self):
        """✅ Vérifie que dark_palette() retourne un QPalette."""
        palette = theme.get_dark_palette()
        assert isinstance(palette, QPalette), "❌ dark_palette() ne retourne pas un QPalette"

    def test_light_palette_is_valid(self):
        """✅ Vérifie que light_palette() retourne un QPalette."""
        palette = theme.get_light_palette()
        assert isinstance(palette, QPalette), "❌ light_palette() ne retourne pas un QPalette"


class TestThemeUtils:

    def test_save_and_load_theme_preference(self):
        """🧪 Vérifie que la sauvegarde/lecture du mode sombre fonctionne."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "theme_config.json")

            theme_utils.save_theme_pref(True, config_path=config_path)
            result = theme_utils.load_theme_pref(config_path=config_path)

            assert result is True, f"❌ Préférence lue incorrecte : {result}"

    def test_default_load_returns_false(self):
        """✅ Vérifie que la lecture d’un fichier inexistant retourne False (valeur par défaut)."""
        result = theme_utils.load_theme_pref(config_path="non_existent_config.json")
        assert result is False, f"❌ Valeur par défaut inattendue : {result}"
