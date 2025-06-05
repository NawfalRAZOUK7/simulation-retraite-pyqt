"""
test_fileio.py

Teste toutes les fonctions d’import/export/config du projet :
- Export et import CSV (shape, contenu)
- Gestion des caractères spéciaux
- Save/Load config JSON
- Robustesse aux erreurs de chemin/fichier
"""

import os
import unittest
import pandas as pd
from utils.fileio import export_csv, load_config, save_config

class TestFileIO(unittest.TestCase):

    def setUp(self):
        self.csv_path = 'data/output/test_export.csv'
        self.csv_path_special = 'data/output/test_export_special.csv'
        self.config_path = 'data/config/test_param.json'

    def tearDown(self):
        for path in [self.csv_path, self.csv_path_special, self.config_path]:
            if os.path.exists(path):
                os.remove(path)

    def test_export_csv(self):
        """Vérifie l’export d’un DataFrame en CSV (shape et contenu)."""
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        result = export_csv(df, self.csv_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.csv_path))
        # Vérification du contenu
        df2 = pd.read_csv(self.csv_path)
        self.assertEqual(df2.shape, df.shape)
        self.assertTrue((df2['col1'] == df['col1']).all())

    def test_import_existing_csv(self):
        """Vérifie qu’on peut relire un CSV exporté précédemment (structure, contenu)."""
        df = pd.DataFrame({'a': [10, 20], 'b': [30, 40]})
        df.to_csv(self.csv_path, index=False)
        df_loaded = pd.read_csv(self.csv_path)
        self.assertEqual(df_loaded.shape, df.shape)
        self.assertListEqual(list(df_loaded.columns), list(df.columns))

    def test_export_import_special_chars(self):
        """Test d’un DataFrame avec caractères spéciaux."""
        df = pd.DataFrame({'col': ['éèàç', '测试', '💡', "O'Reilly"]})
        result = export_csv(df, self.csv_path_special)
        self.assertTrue(result)
        df2 = pd.read_csv(self.csv_path_special)
        self.assertTrue(df2['col'].str.contains('éèàç').any())
        self.assertTrue(df2['col'].str.contains('💡').any())

    def test_save_and_load_config_json(self):
        """Teste la sauvegarde et le chargement d’un fichier config JSON."""
        config = {'IX': 111, 'IY': 222, 'IZ': 333, 'export_path': 'data/output/'}
        self.assertTrue(save_config(config, self.config_path))
        loaded = load_config(self.config_path)
        self.assertEqual(loaded['IX'], 111)
        self.assertEqual(loaded['export_path'], 'data/output/')

    def test_export_non_existing_folder(self):
        """Teste le comportement si le dossier d’export n’existe pas (doit être créé)."""
        temp_dir = 'data/output/tmp_for_test'
        path = os.path.join(temp_dir, 'file.csv')
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        df = pd.DataFrame({'x': [1]})
        result = export_csv(df, path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(path))
        os.remove(path)
        os.rmdir(temp_dir)

    def test_export_empty_dataframe(self):
        """Teste l’export d’un DataFrame vide AVEC colonnes (bonne pratique)."""
        df = pd.DataFrame(columns=['A', 'B', 'C'])
        result = export_csv(df, self.csv_path)
        self.assertTrue(result)
        df2 = pd.read_csv(self.csv_path)
        self.assertEqual(df2.shape, (0, 3))
        self.assertListEqual(list(df2.columns), ['A', 'B', 'C'])

if __name__ == '__main__':
    unittest.main()
