"""
test_stats.py

📊 Teste les fonctions statistiques du module utils.stats :
- Calcul de la moyenne et de l’écart-type
- Calcul de l’intervalle de confiance à 95%
- Comportement face à des données vides ou constantes

🔍 Ces tests garantissent la validité des calculs utilisés
dans l’analyse des 40 simulations de retraite.
"""

import pytest
from utils import stats


class TestStats:

    def test_mean_of_known_values(self):
        """🧪 Vérifie que la moyenne est correcte pour un jeu simple."""
        data = [100, 200, 300, 400]
        result = stats.mean(data)
        assert result == 250, f"❌ Moyenne incorrecte : {result}"

    def test_std_dev_of_known_values(self):
        """🧪 Vérifie l’écart-type (exemple standard connu)."""
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        result = stats.standard_deviation(data)
        assert round(result, 2) == 2.14, f"❌ Écart-type incorrect : {result:.2f}"

    def test_confidence_interval(self):
        """📈 Vérifie le calcul de l’intervalle de confiance à 95%."""
        data = [100, 105, 95, 102, 98, 101, 97, 99, 100, 103]
        mean_value, lower, upper = stats.confidence_interval(data, z=1.96)

        assert isinstance(mean_value, float), "❌ La moyenne n’est pas un float"
        assert lower < mean_value < upper, "❌ Intervalle incohérent"
        assert round(mean_value, 1) == 100.0, f"❌ Moyenne inattendue : {mean_value}"

    def test_empty_data_raises(self):
        """⚠️ Vérifie qu’une exception est levée si la liste est vide."""
        with pytest.raises(ValueError, match=".*vide.*|.*empty.*"):
            stats.mean([])

        with pytest.raises(ValueError):
            stats.standard_deviation([])

        with pytest.raises(ValueError):
            stats.confidence_interval([])

    def test_constant_data_std_zero(self):
        """🧪 Vérifie que l’écart-type de valeurs constantes est 0, et que l’intervalle est fixe."""
        data = [42, 42, 42, 42]
        std_dev = stats.standard_deviation(data)
        assert std_dev == 0.0, f"❌ Écart-type attendu : 0, obtenu : {std_dev}"

        mean_value, lower, upper = stats.confidence_interval(data)
        assert mean_value == 42
        assert lower == upper == 42, f"❌ Intervalle incorrect : [{lower}, {upper}]"
