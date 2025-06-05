"""
test_structure.py

Vérifie l’architecture de base du projet :
- Présence des dossiers data/config/ et data/output/
- Capacité à écrire et supprimer un fichier dans ces dossiers
- (Optionnel) Présence du fichier de config principal

Ce test garantit que le projet démarre sans bug d’environnement,
et que les exports/sauvegardes sont toujours possibles.
"""

import os
import unittest

class TestStructure(unittest.TestCase):
    def test_config_folder_exists(self):
        """Le dossier data/config/ doit exister."""
        self.assertTrue(os.path.exists('data/config/'), "Le dossier data/config/ est manquant.")

    def test_output_folder_exists(self):
        """Le dossier data/output/ doit exister."""
        self.assertTrue(os.path.exists('data/output/'), "Le dossier data/output/ est manquant.")

    def test_write_and_delete_temp_in_config(self):
        """On doit pouvoir écrire puis supprimer un fichier temporaire dans data/config/."""
        path = 'data/config/test_tmp.txt'
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("test")
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.remove(path)
        self.assertFalse(os.path.exists(path), "Le fichier temporaire n'a pas été supprimé.")

    def test_write_and_delete_temp_in_output(self):
        """On doit pouvoir écrire puis supprimer un fichier temporaire dans data/output/."""
        path = 'data/output/test_tmp.txt'
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("test")
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.remove(path)
        self.assertFalse(os.path.exists(path), "Le fichier temporaire n'a pas été supprimé.")

    def test_config_file_exists_after_settings(self):
        """
        (Optionnel) Vérifie que le fichier parametres.json existe après passage dans SettingsWindow.
        À activer seulement si tu lances SettingsWindow en test ou après une config.
        """
        path = 'data/config/parametres.json'
        if os.path.exists(path):
            self.assertTrue(os.path.isfile(path), "Le fichier parametres.json n'est pas un fichier.")
        else:
            self.skipTest("parametres.json n'existe pas encore (lance SettingsWindow une fois pour le créer).")

if __name__ == '__main__':
    unittest.main()
