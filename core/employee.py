# core/employee.py

from core.logger import logger

class Employee:
    def __init__(self, emp_id, age, salaire, date_embauche):
        self.id = emp_id
        self.age = age
        self.salaire = salaire
        self.date_embauche = date_embauche  # année d'embauche (int, ex: 2015)
        self.annees_travaillees = 0  # sera mis à jour dans la simulation
        logger.debug(f"Création Employé #{self.id} | Âge: {self.age}, Salaire: {self.salaire}, Embauche: {self.date_embauche}")

    def avancer_age(self):
        """Fait vieillir l'employé d'un an et incrémente les années travaillées."""
        self.age += 1
        self.annees_travaillees += 1
        logger.debug(f"Employé #{self.id} vieillit → {self.age} ans, {self.annees_travaillees} années travaillées")

    def augmenter_salaire(self, pourcentage=0.05):
        """Augmente le salaire de x% (par défaut 5%)."""
        ancien = self.salaire
        self.salaire *= (1 + pourcentage)
        logger.debug(f"Employé #{self.id} salaire augmenté : {ancien:.2f} → {self.salaire:.2f}")

    def cotisation(self, taux):
        """Renvoie le montant de la cotisation annuelle selon le taux fourni."""
        montant = self.salaire * taux * 12
        logger.debug(f"Employé #{self.id} cotisation calculée à taux {taux:.2%} : {montant:.2f} dh/an")
        return montant

    def est_a_la_retraite(self, age_retraite):
        """Renvoie True si l'employé atteint l'âge de la retraite."""
        retraite = self.age >= age_retraite
        logger.debug(f"Employé #{self.id} atteint retraite ? {retraite} (âge: {self.age}, seuil: {age_retraite})")
        return retraite

    def __repr__(self):
        return f"<Employee #{self.id}: {self.age} ans, {self.salaire:.0f} dh/an, embauché {self.date_embauche}>"
