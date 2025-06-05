# core/retiree.py

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

    def calculer_pension(self, formule_taux=2.0):
        """
        Calcule la pension selon la formule:
            Pension = ((NAT * taux) / 100) * DSAR
        - NAT = nombre d'années travaillées
        - DSAR = dernier salaire avant la retraite
        - taux : 2.0 ou 1.5 (selon le scénario)
        """
        return ((self.annees_travaillees * formule_taux) / 100.0) * self.ancien_salaire

    def __repr__(self):
        return f"<Retiree #{self.id}: retraite à {self.age_retraite} ans, pension {self.pension:.0f} dh/an>"

