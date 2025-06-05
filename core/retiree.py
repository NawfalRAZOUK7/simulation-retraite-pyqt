# core/retiree.py

from core.logger import logger

class Retiree:
    def __init__(self, emp_id, age_retraite, ancien_salaire, annees_travaillees, formule_taux=2.0):
        """
        - emp_id : identifiant unique (int)
        - age_retraite : âge de départ à la retraite (int)
        - ancien_salaire : dernier salaire avant la retraite (float)
        - annees_travaillees : années travaillées avant la retraite (int)
        - formule_taux : pourcentage utilisé pour le calcul (ex: 2.0 ou 1.5)
        """
        self.id = emp_id
        self.age_retraite = age_retraite
        self.ancien_salaire = ancien_salaire
        self.annees_travaillees = annees_travaillees
        self.pension = self.calculer_pension(formule_taux)

        logger.info(f"Création Retraité #{self.id} | âge retraite: {self.age_retraite}, années: {self.annees_travaillees}, pension: {self.pension:.2f} dh")

    def calculer_pension(self, formule_taux=2.0):
        """
        Calcule la pension selon la formule:
            Pension = ((NAT * taux) / 100) * DSAR
        - NAT = nombre d'années travaillées
        - DSAR = dernier salaire avant la retraite
        - taux : 2.0 ou 1.5 (selon le scénario)
        """
        pension = ((self.annees_travaillees * formule_taux) / 100.0) * self.ancien_salaire
        logger.debug(f"Calcul pension pour Retraité #{self.id} : taux={formule_taux} → pension={pension:.2f} dh")
        return pension

    def __repr__(self):
        return f"<Retiree #{self.id}: retraite à {self.age_retraite} ans, pension {self.pension:.0f} dh/an>"
