import pandas as pd
import numpy as np
from core.employee import Employee
from core.retiree import Retiree
from core.scenario import SCENARIOS
from core.germes import GermesAlea
from core.logger import logger  # ✅ logger partagé (DRY)

class Simulator:
    def __init__(self, seed=None, scenario_id=1, IX=12345, IY=23456, IZ=34567, seed_increment=5):
        # Permet de choisir le scénario directement par ID
        self.scenario = SCENARIOS[scenario_id]

        # Priorité au `seed` s'il est fourni
        if seed is not None:
            IX = seed
            IY = seed + 1
            IZ = seed + 2

        self.germes = GermesAlea(IX, IY, IZ)
        self.seed_increment = seed_increment
        self.employes = []
        self.retraites = []
        self.reserve = 200_000_000  # 200 Mdhs
        self._last_result = {}  # Pour les tests anciens
        self.history = []       # Pour les tests anciens

        try:
            self.init_employes()
            self.init_retraites()
            logger.info("Initialisation Simulator (scenario_id=%s, germes=[%d,%d,%d]) OK", scenario_id, IX, IY, IZ)
        except Exception as e:
            logger.error("Erreur à l'initialisation du Simulator: %s", str(e))
            raise

    def init_employes(self):
        self.employes = []
        nb_employes = 10_000
        tranches_age = [(53, 63), (41, 52), (31, 40), (21, 30)]
        freq_age = [0.2, 0.3, 0.3, 0.2]
        ages = []
        for (a_min, a_max), freq in zip(tranches_age, freq_age):
            n = int(nb_employes * freq)
            ages.extend(np.random.randint(a_min, a_max+1, n))
        np.random.shuffle(ages)

        tranches_sal = [
            (24000, 32000),  # 5%
            (16000, 24000),  # 5%
            (12000, 16000),  # 10%
            (8000, 12000),  # 20%
            (6000, 8000),   # 20%
            (4000, 6000),   # 20%
            (3000, 4000),   # 20%
        ]
        freq_sal = [0.05, 0.05, 0.10, 0.20, 0.20, 0.20, 0.20]
        salaires = []
        for (s_min, s_max), freq in zip(tranches_sal, freq_sal):
            n = int(nb_employes * freq)
            salaires.extend(np.random.randint(s_min, s_max+1, n))
        np.random.shuffle(salaires)

        for i in range(nb_employes):
            age = ages[i]
            salaire = salaires[i]
            date_embauche = 2025 - (age - 21)
            emp = Employee(emp_id=i+1, age=age, salaire=salaire, date_embauche=date_embauche)
            self.employes.append(emp)
        logger.debug("init_employes: %d employés générés", len(self.employes))

    def init_retraites(self):
        self.retraites = []
        for i in range(1_000):
            age_retraite = int(63 + self.germes.alea() * 10)
            ancien_salaire = int(3000 + self.germes.alea() * (40000 - 3000))
            annees_travaillees = age_retraite - 21
            ret = Retiree(
                emp_id=10_001 + i,
                age_retraite=age_retraite,
                ancien_salaire=ancien_salaire,
                annees_travaillees=annees_travaillees,
                formule_taux=self.scenario.formule_taux_pension
            )
            self.retraites.append(ret)
        logger.debug("init_retraites: %d retraités générés", len(self.retraites))

    def _generate_nouveaux_recrues(self, n_recrues, annee):
        tranches_age = [(21, 24), (25, 28), (29, 32), (33, 36), (37, 40), (41, 45)]
        freq_age = [0.05, 0.30, 0.30, 0.15, 0.15, 0.05]
        ages = []
        for (a_min, a_max), freq in zip(tranches_age, freq_age):
            n = int(n_recrues * freq)
            ages.extend(np.random.randint(a_min, a_max+1, n))
        while len(ages) < n_recrues:
            ages.append(np.random.randint(21, 46))
        np.random.shuffle(ages)

        tranches_sal = [
            (24000, 32000), (16000, 24000), (12000, 16000),
            (8000, 12000), (6000, 8000), (4000, 6000), (3000, 4000),
        ]
        freq_sal = [0.05, 0.05, 0.10, 0.20, 0.20, 0.20, 0.20]
        salaires = []
        for (s_min, s_max), freq in zip(tranches_sal, freq_sal):
            n = int(n_recrues * freq)
            salaires.extend(np.random.randint(s_min, s_max+1, n))
        while len(salaires) < n_recrues:
            salaires.append(np.random.randint(3000, 32001))
        np.random.shuffle(salaires)

        new_emps = []
        for i in range(n_recrues):
            age = ages[i]
            salaire = salaires[i]
            emp = Employee(emp_id=len(self.employes) + len(new_emps) + 1, age=age, salaire=salaire, date_embauche=annee)
            new_emps.append(emp)
        logger.debug("Nouveaux recrutés générés : %d (année %d)", n_recrues, annee)
        return new_emps

    def simuler_annee(self, annee):
        scenario = self.scenario

        # Augmentation salariale tous les 5 ans
        if (annee - 2025) % 5 == 0:
            for emp in self.employes:
                emp.augmenter_salaire()

        # Recrutement
        logger.debug("Valeur alea germes: %.5f", self.germes.alea())
        n_recrues = 300  # fixe pour test
        new_emps = self._generate_nouveaux_recrues(n_recrues, annee)
        self.employes.extend(new_emps)

        # Départs à la retraite
        nouveaux_retraites = [emp for emp in self.employes if emp.est_a_la_retraite(scenario.age_retraite)]
        for emp in nouveaux_retraites:
            ret = Retiree(emp.id, emp.age, emp.salaire, emp.annees_travaillees, scenario.formule_taux_pension)
            self.retraites.append(ret)
        self.employes = [emp for emp in self.employes if not emp.est_a_la_retraite(scenario.age_retraite)]

        # Vieillissement
        for emp in self.employes:
            emp.avancer_age()

        # Calculs financiers
        tot_cotis = sum(emp.cotisation(scenario.get_taux_cotisation(emp.salaire)) for emp in self.employes)
        tot_pens = sum(ret.pension for ret in self.retraites)
        self.reserve += tot_cotis - tot_pens

        # Résultat
        result = {
            "TotEmp": len(self.employes),
            "TotRet": len(self.retraites),
            "TotCotis": tot_cotis,
            "TotPens": tot_pens,
            "Reserve": self.reserve,
            "NouvRet": len(nouveaux_retraites),
            "NouvRec": n_recrues,
        }
        self._last_result = result  # 🔁 pour les anciens tests
        return result

    def simuler_11_ans(self, simulation_id=None):
        donnees = []
        for year in range(2025, 2025 + 11):
            result = self.simuler_annee(year)
            result["Annee"] = year
            if simulation_id is not None:
                result["Simulation"] = simulation_id
            donnees.append(result)
        df = pd.DataFrame(donnees)
        self.history = df.to_dict(orient="records")  # 🔁 pour compatibilité
        logger.debug("simuler_11_ans: Simulation sur 11 ans terminée.")
        return df

    def simuler_40_runs(self):
        all_runs = []
        initial_germes = self.germes.get_germes()
        logger.info("Début simuler_40_runs (scenario=%s, germes init=%s)", self.scenario.nom, initial_germes)
        try:
            for i in range(40):
                self.germes.set_germes(*initial_germes)
                for _ in range(i):
                    self.germes.next_germes()
                self.init_employes()
                self.init_retraites()
                self.reserve = 200_000_000
                df_run = self.simuler_11_ans(simulation_id=i + 1)
                all_runs.append(df_run)
                logger.debug("Run %d/40 terminé.", i + 1)
            logger.info("simuler_40_runs : Simulation complète (40 runs)")
        except Exception as e:
            logger.error("Erreur pendant simuler_40_runs : %s", str(e))
            raise

        # ✅ Solution ici :
        self.dernier_resultat_df = pd.concat(all_runs, ignore_index=True)

        return all_runs

    # --- Aliases pour compatibilité descendante avec anciens tests ---
    def get_indicator(self, name):
        """Retourne la dernière valeur de l’indicateur demandé après une simulation annuelle."""
        try:
            return self._last_result[name]
        except (AttributeError, KeyError):
            raise ValueError(f"Indicateur inconnu ou simulation non encore exécutée : {name}")

    def run_one_year(self):
        """Alias pour simuler une seule année (2025)."""
        self._last_result = self.simuler_annee(2025)

    def run_full_simulation(self):
        """Alias pour simulation sur 11 ans (résultats accessibles via .history)."""
        self.history = self.simuler_11_ans().to_dict(orient="records")


# Exemple d'utilisation :
# sim = Simulator(seed=123, scenario_id=1)
# df = sim.simuler_11_ans()
# runs = sim.simuler_40_runs()
# df_concat = pd.concat(runs, ignore_index=True)
