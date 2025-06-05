"""
test_stats.py

Teste les fonctions statistiques du module utils.stats :
- Calcul de la moyenne et de l’écart-type
- Calcul de l’intervalle de confiance à 95%
- Comportement face à des données vides ou constantes

Ces tests garantissent la validité des calculs utilisés dans l’analyse des 40 simulations.
"""

import pytest
from utils import stats


class TestStats:
    def test_mean_of_known_values(self):
        """Teste la moyenne d’une série de valeurs connues."""
        data = [100, 200, 300, 400]
        result = stats.mean(data)
        assert result == 250

    def test_std_dev_of_known_values(self):
        """Teste l’écart-type sur un jeu de données connu."""
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = stats.standard_deviation(data)
        assert round(result, 2) == 2.14  # Écart-type empirique

    def test_confidence_interval(self):
        """Teste l’intervalle de confiance à 95% avec des données simulées."""
        data = [100, 105, 95, 102, 98, 101, 97, 99, 100, 103]
        mean_value, lower, upper = stats.confidence_interval(data, z=1.96)

        assert isinstance(mean_value, float)
        assert lower < mean_value < upper
        assert round(mean_value, 1) == 100.0  # attendu environ

    def test_empty_data_raises(self):
        """Vérifie qu’une exception est levée avec une liste vide."""
        with pytest.raises(ValueError):
            stats.mean([])

        with pytest.raises(ValueError):
            stats.standard_deviation([])

        with pytest.raises(ValueError):
            stats.confidence_interval([])

    def test_constant_data_std_zero(self):
        """Teste le cas où toutes les valeurs sont identiques (σ = 0)."""
        data = [42, 42, 42, 42]
        std_dev = stats.standard_deviation(data)
        assert std_dev == 0.0

        mean_value, lower, upper = stats.confidence_interval(data)
        assert mean_value == 42
        assert lower == upper == 42
