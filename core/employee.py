# core/employee.py

class Employee:
    def __init__(self, emp_id, age, salaire, date_embauche):
        self.id = emp_id
        self.age = age
        self.salaire = salaire
        self.date_embauche = date_embauche  # année d'embauche (int, ex: 2015)
        self.annees_travaillees = 0  # sera mis à jour dans la simulation

    def avancer_age(self):
        """Fait vieillir l'employé d'un an et incrémente les années travaillées."""
        self.age += 1
        self.annees_travaillees += 1

    def augmenter_salaire(self, pourcentage=0.05):
        """Augmente le salaire de x% (par défaut 5%)."""
        self.salaire *= (1 + pourcentage)

    def cotisation(self, taux):
        """Renvoie le montant de la cotisation annuelle selon le taux fourni."""
        return self.salaire * taux * 12  # 12 mois

    def est_a_la_retraite(self, age_retraite):
        """Renvoie True si l'employé atteint l'âge de la retraite."""
        return self.age >= age_retraite

    def __repr__(self):
        return f"<Employee #{self.id}: {self.age} ans, {self.salaire:.0f} dh/an, embauché {self.date_embauche}>"

