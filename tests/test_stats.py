"""
test_stats.py

Teste les fonctions statistiques (moyenne, intervalle de confiance, robustesse) :
- Moyenne sur listes simples ou DataFrame
- Intervalle de confiance 95% sur données connues (listes et DataFrame)
- Cas limites (liste vide, un seul élément)
- Cohérence entre calculs manuels et via DataFrame
- Tests spécifiques : IC par année (intervalle_confiance_reserve), IC multi-années (intervalle_confiance_multi)
"""

import unittest
import pandas as pd
from utils.stats import (
    moyenne_reserve,
    intervalle_confiance,
    intervalle_confiance_reserve,
    intervalle_confiance_multi
)

class TestStats(unittest.TestCase):

    def test_moyenne_simple(self):
        """Moyenne sur une liste simple."""
        data = [100, 200, 300]
        self.assertAlmostEqual(moyenne_reserve(data), 200)

    def test_moyenne_dataframe(self):
        """Moyenne via une DataFrame Reserve."""
        df = pd.DataFrame({'Reserve': [10, 20, 30]})
        self.assertAlmostEqual(moyenne_reserve(df), 20)

    def test_moyenne_dataframe_par_annee(self):
        """Moyenne via une DataFrame filtrée par année."""
        df = pd.DataFrame({
            'Annee': [2020, 2020, 2021],
            'Reserve': [100, 200, 300]
        })
        self.assertAlmostEqual(moyenne_reserve(df, annee=2020), 150)
        self.assertAlmostEqual(moyenne_reserve(df, annee=2021), 300)

    def test_intervalle_confiance_valeurs_connues(self):
        """IC 95% sur un jeu de données connu (liste simple)."""
        data = [100, 200, 300, 400, 500]
        ic_low, ic_high = intervalle_confiance(data, alpha=0.05)
        self.assertTrue(ic_low < sum(data)/len(data) < ic_high)
        # Vérification robuste avec assertAlmostEqual (tolérance 2 unités)
        self.assertAlmostEqual(ic_low, 103.01, delta=2)
        self.assertAlmostEqual(ic_high, 496.99, delta=2)

    def test_ic_single_element(self):
        """Cas limite : IC sur une liste à un seul élément."""
        data = [123]
        ic_low, ic_high = intervalle_confiance(data, alpha=0.05)
        self.assertEqual(ic_low, ic_high)
        self.assertEqual(ic_low, 123)

    def test_ic_empty(self):
        """Cas limite : IC sur une liste vide ou None."""
        ic_low, ic_high = intervalle_confiance([], alpha=0.05)
        self.assertIsNone(ic_low)
        self.assertIsNone(ic_high)
        ic_low, ic_high = intervalle_confiance(None, alpha=0.05)
        self.assertIsNone(ic_low)
        self.assertIsNone(ic_high)

    def test_moyenne_vs_dataframe(self):
        """Cohérence entre moyenne brute et via DataFrame."""
        data = [100, 200, 300, 400]
        moyenne1 = moyenne_reserve(data)
        df = pd.DataFrame({'Reserve': data})
        moyenne2 = moyenne_reserve(df['Reserve'])
        self.assertAlmostEqual(moyenne1, moyenne2)

    # ----------- Tests spécifiques ajoutés -----------

    def test_ic_reserve_dataframe(self):
        """IC via DataFrame pour une année donnée."""
        df = pd.DataFrame({
            'Annee': [2020, 2020, 2021, 2021, 2021],
            'Reserve': [100, 200, 300, 400, 500]
        })
        ic_low, ic_high = intervalle_confiance_reserve(df, annee=2021, alpha=0.05)
        self.assertTrue(ic_low < 400 < ic_high)  # moyenne de 2021 = 400

    def test_ic_multi(self):
        """IC multi-années via DataFrame."""
        df = pd.DataFrame({
            'Annee': [2020, 2020, 2021, 2021, 2021],
            'Reserve': [100, 200, 300, 400, 500]
        })
        result = intervalle_confiance_multi(df, [2020, 2021], alpha=0.05)
        self.assertIn(2020, result)
        self.assertIn(2021, result)
        ic_2020 = result[2020]
        ic_2021 = result[2021]
        self.assertTrue(ic_2020[0] < 150 < ic_2020[1])   # moyenne 2020 = 150
        self.assertTrue(ic_2021[0] < 400 < ic_2021[1])   # moyenne 2021 = 400

if __name__ == '__main__':
    unittest.main()
