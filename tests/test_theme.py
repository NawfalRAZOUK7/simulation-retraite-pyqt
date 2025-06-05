"""
test_theme.py

Teste les composants de gestion du thème :
- Génération des palettes claire et sombre (fonctions du module ui.theme)
- Sauvegarde et chargement des préférences utilisateur (utils.theme_utils)

Ces tests garantissent que le thème de l’application peut être modifié, sauvegardé
et restauré correctement d’une session à l’autre.
"""

import os
import tempfile
import pytest
from PyQt5.QtGui import QPalette
from ui import theme
from utils import theme_utils


class TestThemePalettes:
    def test_dark_palette_is_valid(self):
        """Teste que la palette sombre retourne bien un objet QPalette."""
        palette = theme.dark_palette()
        assert isinstance(palette, QPalette)

    def test_light_palette_is_valid(self):
        """Teste que la palette claire retourne bien un objet QPalette."""
        palette = theme.light_palette()
        assert isinstance(palette, QPalette)


class TestThemeUtils:
    def test_save_and_load_theme_preference(self):
        """Teste la sauvegarde et la lecture d’un thème (dans fichier temporaire)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_config = os.path.join(temp_dir, "theme_config.json")

            # Sauvegarder préférence (ex: "dark")
            theme_utils.save_theme_preference("dark", config_path=temp_config)

            # Lire la préférence
            result = theme_utils.load_theme_preference(config_path=temp_config)
            assert result == "dark"

    def test_default_load_returns_string(self):
        """Teste que la lecture sans fichier retourne bien une chaîne (ex: 'light')."""
        # Fichier inexistant → doit retourner une valeur sûre
        result = theme_utils.load_theme_preference(config_path="non_existent_config.json")
        assert isinstance(result, str)
