"""
test_simulator.py

Teste le cœur de la simulation :
- Initialisation du simulateur avec des germes (IX, IY, IZ)
- Exécution d’une simulation sur une ou plusieurs années
- Vérification des indicateurs calculés (TotEmp, TotRet, Reserve, etc.)
- Robustesse de la logique face à des scénarios connus

Ce test garantit que la logique métier principale fonctionne,
et que l’évolution des états est cohérente dans le temps.
"""

import pytest
from core.simulator import Simulator
from core.scenario import Scenario


class TestSimulatorCore:
    def test_initialization_with_seeds(self):
        """Teste que le simulateur s’initialise correctement avec des germes fixés."""
        sim = Simulator(seed_x=100, seed_y=200, seed_z=300, scenario_id=1)
        assert sim is not None
        assert hasattr(sim, "employees")
        assert hasattr(sim, "retirees")
        assert isinstance(sim.year, int)
        assert sim.year == 2025

    def test_run_one_year_simulation(self):
        """Teste que la simulation d’une année met à jour les états."""
        sim = Simulator(seed_x=100, seed_y=200, seed_z=300, scenario_id=1)
        initial_tot_emp = sim.get_indicator("TotEmp")
        initial_retirees = sim.get_indicator("TotRet")
        initial_reserve = sim.get_indicator("Reserve")

        sim.run_one_year()

        updated_tot_emp = sim.get_indicator("TotEmp")
        updated_retirees = sim.get_indicator("TotRet")
        updated_reserve = sim.get_indicator("Reserve")

        # Attendu : évolution (non stricte, mais des changements)
        assert updated_tot_emp != initial_tot_emp or updated_retirees != initial_retirees
        assert isinstance(updated_reserve, float)

    def test_run_full_simulation_11_years(self):
        """Teste qu’une simulation complète de 11 ans s’exécute sans erreur."""
        sim = Simulator(seed_x=100, seed_y=200, seed_z=300, scenario_id=2)
        sim.run_full_simulation()

        # Doit contenir 11 entrées d’indicateurs
        assert len(sim.history) == 11
        assert all("TotEmp" in year_data for year_data in sim.history)

    def test_scenario_effects(self):
        """Teste l’impact d’un scénario avec cotisation/pension modifiées (ex: scénario 4)."""
        sim = Simulator(seed_x=101, seed_y=201, seed_z=301, scenario_id=4)
        sim.run_one_year()

        reserve = sim.get_indicator("Reserve")
        pension = sim.get_indicator("TotPens")
        cotisations = sim.get_indicator("TotCotis")

        assert reserve > 0
        assert cotisations > 0
        assert pension > 0
