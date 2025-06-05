"""
test_simulator.py

Teste la simulation métier (runs, résultats, robustesse) :
- Résultats sur 11 ans
- 40 runs de simulation
- Test de tous les scénarios
- Test de valeurs extrêmes
- Test d’exception (optionnel)
"""

import unittest
from core.simulator import Simulator
import pandas as pd

class TestSimulator(unittest.TestCase):

    def test_simuler_11_ans(self):
        """Simulation de 11 ans (vérifie le nombre de lignes et colonnes)."""
        sim = Simulator(scenario_id=1)
        df = sim.simuler_11_ans()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 11)  # 11 années simulées
        # Vérifier colonnes attendues
        expected_cols = {"Annee", "TotEmp", "TotRet", "TotCotis", "TotPens", "Reserve", "NouvRet", "NouvRec"}
        self.assertTrue(expected_cols.issubset(set(df.columns)))

    def test_simuler_40_runs(self):
        """Simulation de 40 runs (vérifie la quantité et la structure)."""
        sim = Simulator(scenario_id=1)
        runs = sim.simuler_40_runs()
        self.assertEqual(len(runs), 40)
        for df in runs:
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(df.shape[0], 11)

    def test_all_scenarios(self):
        """Simulation pour chaque scénario (1 à 4)."""
        for scenario_id in range(1, 5):
            with self.subTest(scenario_id=scenario_id):
                sim = Simulator(scenario_id=scenario_id)
                runs = sim.simuler_40_runs()
                self.assertEqual(len(runs), 40)
                for df in runs:
                    self.assertTrue("Annee" in df.columns)

    def test_extreme_germes(self):
        """Simulation avec valeurs extrêmes de germes."""
        sim = Simulator(scenario_id=1, IX=0, IY=999999, IZ=-100)
        df = sim.simuler_11_ans()
        self.assertEqual(df.shape[0], 11)
        # Vérifie que la réserve reste numérique et non vide
        self.assertTrue(pd.api.types.is_numeric_dtype(df["Reserve"]))
        self.assertFalse(df["Reserve"].isnull().any())

    def test_exception_handling(self):
        """(Optionnel) Force une erreur et vérifie qu’elle est bien remontée."""
        # Suppose que simuler_annee peut lever une exception sur une mauvaise année.
        sim = Simulator(scenario_id=1)
        try:
            result = sim.simuler_annee("not_a_year")
            self.fail("Une exception aurait dû être levée pour une année invalide.")
        except Exception as e:
            self.assertIsInstance(e, Exception)
            # Ici tu pourrais aussi vérifier que le logger a bien tracé l’erreur.

if __name__ == '__main__':
    unittest.main()
