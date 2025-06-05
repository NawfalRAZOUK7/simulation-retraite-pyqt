# tests/test_simulator.py

"""
🎯 Teste le cœur de la simulation :
- Initialisation du simulateur
- Exécution d’une simulation sur une ou plusieurs années
- Vérification des indicateurs calculés (TotEmp, TotRet, Reserve, etc.)
- Robustesse de la logique face à des scénarios connus

🧠 Ce test garantit que la logique métier principale fonctionne,
et que l’évolution des états est cohérente dans le temps.
"""

import pytest
from core.simulator import Simulator

class TestSimulatorCore:

    def test_initialization(self):
        sim = Simulator(seed=123, scenario_id=1)
        sim.run_one_year()  # ✅ Ajouté pour remplir les indicateurs
        assert sim is not None, "❌ Le simulateur n’a pas été créé"
        assert isinstance(sim.get_indicator("TotEmp"), int), "❌ L’indicateur 'TotEmp' devrait exister après init"
        assert isinstance(sim.get_indicator("TotRet"), int), "❌ L’indicateur 'TotRet' devrait exister après init"
        assert isinstance(sim.get_indicator("Reserve"), float), "❌ 'Reserve' doit être un float"

    def test_run_one_year_simulation(self):
        sim = Simulator(seed=123, scenario_id=1)
        sim.run_one_year()
        initial_tot_emp = sim.get_indicator("TotEmp")
        initial_retirees = sim.get_indicator("TotRet")
        initial_reserve = sim.get_indicator("Reserve")

        sim.run_one_year()  # ✅ Nouvelle année
        updated_tot_emp = sim.get_indicator("TotEmp")
        updated_retirees = sim.get_indicator("TotRet")
        updated_reserve = sim.get_indicator("Reserve")

        assert updated_tot_emp != initial_tot_emp or updated_retirees != initial_retirees, \
            "❌ Aucune évolution détectée après 1 an"
        assert isinstance(updated_reserve, float), "❌ La réserve doit être un float"

    def test_run_full_simulation_11_years(self):
        sim = Simulator(seed=456, scenario_id=2)
        sim.run_full_simulation()  # ✅ Remplit .history

        assert len(sim.history) == 11, "❌ L’historique ne contient pas 11 années"
        assert all("TotEmp" in year_data for year_data in sim.history), \
            "❌ L’indicateur 'TotEmp' est absent dans une année simulée"

    def test_scenario_effects(self):
        sim = Simulator(seed=789, scenario_id=4)
        sim.run_one_year()
        reserve = sim.get_indicator("Reserve")
        pension = sim.get_indicator("TotPens")
        cotisations = sim.get_indicator("TotCotis")

        assert reserve > 0, "❌ Réserve nulle ou négative"
        assert cotisations > 0, "❌ Aucune cotisation calculée"
        assert pension > 0, "❌ Aucune pension versée"
