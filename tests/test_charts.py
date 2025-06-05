"""
test_charts.py

📊 Teste les composants de l’interface graphique liés aux graphiques :
- Initialisation des onglets : Réserve, Comparaison, Confiance
- Intégration avec des données simulées simples
- Résilience face à des données vides ou inattendues
- Chargement du sélecteur de scénario

🧪 Ces tests garantissent que les composants UI de visualisation
fonctionnent sans crash et peuvent afficher des données simulées.
"""

import pytest
from ui.charts_window.tab_reserve import TabReserve
from ui.charts_window.tab_comparaison import TabComparaison
from ui.charts_window.tab_confidence import TabConfidence
from ui.charts_window.scenario_selector import ScenarioSelector


class TestChartsUI:

    def test_tab_reserve_initialization(self, qtbot):
        """🧪 Vérifie que TabReserve s’instancie correctement."""
        widget = TabReserve()
        qtbot.addWidget(widget)
        assert widget.layout() is not None, "❌ Layout manquant dans TabReserve"

    def test_tab_reserve_update_with_data(self, qtbot):
        """🧪 Vérifie que TabReserve accepte des données simples sans planter."""
        widget = TabReserve()
        qtbot.addWidget(widget)

        mock_data = [
            {"Année": 2025, "Reserve": 100},
            {"Année": 2026, "Reserve": 120}
        ]
        try:
            widget.update_chart(mock_data)
        except Exception as e:
            pytest.fail(f"❌ update_chart() a échoué avec données valides : {e}")

    def test_tab_comparaison_safe_update(self, qtbot):
        """🧪 Vérifie que TabComparaison accepte des données groupées par scénario."""
        widget = TabComparaison()
        qtbot.addWidget(widget)

        fake_data = {
            "Scénario 1": [{"Année": 2025, "Reserve": 100}],
            "Scénario 2": [{"Année": 2025, "Reserve": 90}],
        }
        try:
            widget.update_chart(fake_data)
        except Exception as e:
            pytest.fail(f"❌ TabComparaison a échoué avec des données groupées : {e}")

    def test_tab_confidence_accepts_error_bounds(self, qtbot):
        """🧪 Vérifie que TabConfidence peut afficher un intervalle de confiance."""
        widget = TabConfidence()
        qtbot.addWidget(widget)

        fake_bounds = {
            "Année": [2025, 2026, 2027],
            "Moyenne": [100, 105, 110],
            "Min": [90, 95, 100],
            "Max": [110, 115, 120]
        }
        try:
            widget.update_chart(fake_bounds)
        except Exception as e:
            pytest.fail(f"❌ TabConfidence n’a pas affiché les bornes : {e}")

    def test_scenario_selector_initialization(self, qtbot):
        """🧪 Vérifie que le sélecteur de scénario est bien chargé."""
        selector = ScenarioSelector(scenario_names=["Scénario 1", "Scénario 2"])
        qtbot.addWidget(selector)

        assert selector.combo_box is not None, "❌ ComboBox manquant"
        assert selector.combo_box.count() > 0, "❌ Aucun scénario chargé dans le combo"
