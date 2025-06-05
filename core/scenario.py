# core/scenario.py

from core.logger import logger

class Scenario:
    def __init__(self,
                 nom,
                 age_retraite,
                 taux_cotisation_tranches,
                 formule_taux_pension):
        """
        - nom : nom du scénario (str)
        - age_retraite : âge de départ en retraite (int)
        - taux_cotisation_tranches : dict {tranche_salaire: taux}
        - formule_taux_pension : taux pour le calcul de pension (ex: 2.0 ou 1.5)
        """
        self.nom = nom
        self.age_retraite = age_retraite
        self.taux_cotisation_tranches = taux_cotisation_tranches
        self.formule_taux_pension = formule_taux_pension

        logger.info(f"Scénario chargé: {self.nom}, retraite à {self.age_retraite}, taux pension: {self.formule_taux_pension}")

    def get_taux_cotisation(self, salaire):
        """Retourne le taux de cotisation selon la tranche du salaire."""
        for borne, taux in sorted(self.taux_cotisation_tranches.items()):
            if salaire <= borne:
                logger.debug(f"Salaire {salaire} → taux cotisation = {taux}")
                return taux
        taux_max = list(self.taux_cotisation_tranches.values())[-1]
        logger.debug(f"Salaire {salaire} dépasse toutes les bornes → taux max = {taux_max}")
        return taux_max

    def __repr__(self):
        return f"<Scenario: {self.nom}, retraite à {self.age_retraite} ans, taux_pension={self.formule_taux_pension}>"


# Définition des scénarios (selon l'énoncé)

SCENARIOS = {
    1: Scenario(
        nom="Départ à 63 ans",
        age_retraite=63,
        taux_cotisation_tranches={
            5000: 0.05,
            7000: 0.06,
            10000: 0.08,
            float('inf'): 0.10
        },
        formule_taux_pension=2.0
    ),
    2: Scenario(
        nom="Départ à 65 ans",
        age_retraite=65,
        taux_cotisation_tranches={
            5000: 0.05,
            7000: 0.06,
            10000: 0.08,
            float('inf'): 0.10
        },
        formule_taux_pension=2.0
    ),
    3: Scenario(
        nom="65 ans + cotisation augmentée",
        age_retraite=65,
        taux_cotisation_tranches={
            5000: 0.06,
            7000: 0.08,
            10000: 0.10,
            float('inf'): 0.14
        },
        formule_taux_pension=2.0
    ),
    4: Scenario(
        nom="65 ans + cotisation augmentée + pension réduite",
        age_retraite=65,
        taux_cotisation_tranches={
            5000: 0.06,
            7000: 0.08,
            10000: 0.10,
            float('inf'): 0.14
        },
        formule_taux_pension=1.5
    ),
}

# Exemple d’utilisation
# from core.scenario import SCENARIOS
# sc = SCENARIOS[2]
# taux = sc.get_taux_cotisation(salaire=8300)
