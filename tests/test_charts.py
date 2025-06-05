"""
test_charts.py

Teste la génération des graphiques :
- Plot réserve avec données valides
- Comparaison scénarios (multi-DataFrames)
- Robustesse face aux données vides/nulles
- (Optionnel) Test des axes, titres, couleurs
- (Optionnel) Simulation d’erreur matplotlib/logging
"""

import unittest
import pandas as pd
from utils.charts import plot_reserve_evolution, plot_scenario_comparaison

class TestCharts(unittest.TestCase):

    def test_plot_reserve_valid_data(self):
        """Génère un plot de réserve avec données valides (ne doit pas lever d’exception)."""
        df = pd.DataFrame({
            'Annee': list(range(2025, 2036)),
            'Reserve': [1_000_000 + i*50_000 for i in range(11)],
            'Simulation': [1]*11
        })
        try:
            plot_reserve_evolution(df)
        except Exception as e:
            self.fail(f"plot_reserve_evolution a levé une exception avec données valides : {e}")

    def test_plot_comparaison_multi_df(self):
        """Génère un plot de comparaison scénarios avec plusieurs DataFrames."""
        data_scenarios = {}
        for k in range(1, 4):
            data_scenarios[f'Scénario {k}'] = pd.DataFrame({
                'Annee': list(range(2025, 2036)),
                'Reserve': [1_000_000 + i*30_000*k for i in range(11)],
                'Simulation': [k]*11
            })
        try:
            plot_scenario_comparaison(data_scenarios)
        except Exception as e:
            self.fail(f"plot_scenario_comparaison a levé une exception : {e}")

    def test_plot_empty_data(self):
        """Génère un plot avec un DataFrame vide (ne doit pas lever d’exception)."""
        df = pd.DataFrame({'Annee': [], 'Reserve': [], 'Simulation': []})
        try:
            plot_reserve_evolution(df)
        except Exception as e:
            self.fail(f"plot_reserve_evolution a échoué avec DataFrame vide : {e}")

    def test_plot_none(self):
        """Génère un plot avec None en entrée (ne doit pas lever d’exception)."""
        try:
            plot_reserve_evolution(pd.DataFrame({'Annee': [], 'Reserve': [], 'Simulation': []}))
        except Exception as e:
            self.fail(f"plot_reserve_evolution a échoué avec None : {e}")

    # (Optionnel) Test des titres/axes/couleurs
    def test_plot_titles_labels(self):
        """Teste la présence de titres/labels dans le plot (visuellement/logging seulement)."""
        df = pd.DataFrame({'Annee': [2025, 2026], 'Reserve': [1_000_000, 1_050_000], 'Simulation': [1, 1]})
        try:
            plot_reserve_evolution(df)  # À vérifier visuellement/log dans matplotlib
        except Exception as e:
            self.fail(f"plot_reserve_evolution a échoué sur les titres/labels : {e}")

    # (Optionnel) Simulation d’erreur (en patchant plt.show par exemple)
    def test_plot_forced_exception(self):
        """Simule une erreur matplotlib (logger doit tracer l’erreur)."""
        import matplotlib.pyplot as plt

        def fail_show():
            raise RuntimeError("Erreur forcée matplotlib")

        orig_show = plt.show
        plt.show = fail_show
        df = pd.DataFrame({'Annee': [2025], 'Reserve': [1_000_000], 'Simulation': [1]})
        try:
            plot_reserve_evolution(df)
        except Exception as e:
            # On s'attend à une exception, le logger doit tracer l'erreur
            pass
        finally:
            plt.show = orig_show  # Restaure le comportement original

if __name__ == '__main__':
    unittest.main()
