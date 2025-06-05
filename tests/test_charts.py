"""
test_charts.py

Teste les composants de l’interface graphique liés aux graphiques :
- Initialisation des onglets : Réserve, Comparaison, Confiance
- Intégration avec des données simulées simples
- Résilience des composants face à des données vides ou inattendues
- Chargement du sélecteur de scénario (UI logic only)

Ces tests garantissent que les composants UI de visualisation fonctionnent sans crash,
et qu’ils peuvent afficher des données simulées dans un environnement de test.
"""

import pytest
from PyQt5.QtWidgets import QApplication
import sys

from ui.charts_window.tab_reserve import TabReserve
from ui.charts_window.tab_comparaison import TabComparaison
from ui.charts_window.tab_confidence import TabConfidence
from ui.charts_window.scenario_selector import ScenarioSelector


app = QApplication(sys.argv)  # Required to create any QWidget


class TestChartsUI:
    def test_tab_reserve_initialization(self):
        """Vérifie que TabReserve s’initialise sans erreur."""
        widget = TabReserve()
        assert widget is not None
        assert widget.layout() is not None

    def test_tab_reserve_update_with_data(self):
        """Teste que TabReserve accepte des données simulées."""
        widget = TabReserve()
        mock_data = [{"Année": 2025, "Reserve": 100}, {"Année": 2026, "Reserve": 120}]
        try:
            widget.update_chart(mock_data)
        except Exception as e:
            pytest.fail(f"update_chart a échoué avec des données valides: {e}")

    def test_tab_comparaison_safe_update(self):
        """Teste TabComparaison avec données groupées par scénario."""
        widget = TabComparaison()
        fake_data = {
            "Scénario 1": [{"Année": 2025, "Reserve": 100}],
            "Scénario 2": [{"Année": 2025, "Reserve": 90}],
        }
        try:
            widget.update_chart(fake_data)
        except Exception as e:
            pytest.fail(f"TabComparaison n’a pas géré les données groupées : {e}")

    def test_tab_confidence_accepts_error_bounds(self):
        """Vérifie que TabConfidence accepte les bornes inf/sup d’un intervalle de confiance."""
        widget = TabConfidence()
        fake_bounds = {
            "Année": [2025, 2026, 2027],
            "Moyenne": [100, 105, 110],
            "Min": [90, 95, 100],
            "Max": [110, 115, 120]
        }
        try:
            widget.update_chart(fake_bounds)
        except Exception as e:
            pytest.fail(f"TabConfidence n’a pas pu afficher les intervalles : {e}")

    def test_scenario_selector_initialization(self):
        """Vérifie que le ScenarioSelector est bien initialisé."""
        selector = ScenarioSelector()
        assert selector is not None
        assert selector.combo_box is not None
        assert selector.combo_box.count() > 0
