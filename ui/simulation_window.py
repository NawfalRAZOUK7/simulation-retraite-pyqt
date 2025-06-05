# ui/simulation_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt

from core.simulator import Simulator
from core.scenario import SCENARIOS
import pandas as pd

from ui import logger  # Logger global UI

class SimulationWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lancer une Simulation de Retraite")
        self.setGeometry(250, 250, 480, 350)
        self.init_ui()
        logger.info("SimulationWindow ouverte.")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Configuration de la Simulation")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 24px;")
        layout.addWidget(title_label)

        # Choix du scénario
        self.combo_scenario = QComboBox()
        for k, scenario in SCENARIOS.items():
            self.combo_scenario.addItem(f"{k} — {scenario.nom}", k)
        layout.addWidget(QLabel("Scénario"))
        layout.addWidget(self.combo_scenario)

        # Champs pour les germes
        form = QFormLayout()
        self.edit_ix = QLineEdit("12345")
        self.edit_iy = QLineEdit("23456")
        self.edit_iz = QLineEdit("34567")
        for widget in [self.edit_ix, self.edit_iy, self.edit_iz]:
            widget.setMaximumWidth(120)
        form.addRow("Gemme IX :", self.edit_ix)
        form.addRow("Gemme IY :", self.edit_iy)
        form.addRow("Gemme IZ :", self.edit_iz)
        layout.addLayout(form)

        # Bouton lancer
        self.btn_lancer = QPushButton("Lancer la Simulation")
        self.btn_lancer.setMinimumHeight(40)
        self.btn_lancer.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.btn_lancer)

        self.btn_lancer.clicked.connect(self.lancer_simulation)

    def lancer_simulation(self):
        # Lecture des paramètres utilisateur
        scenario_id = self.combo_scenario.currentData()
        try:
            ix = int(self.edit_ix.text())
            iy = int(self.edit_iy.text())
            iz = int(self.edit_iz.text())
            logger.info("Paramètres simulation : scenario=%s, IX=%d, IY=%d, IZ=%d", scenario_id, ix, iy, iz)
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir des valeurs numériques valides pour les germes.")
            logger.warning("Valeurs de germes invalides saisies par l'utilisateur.")
            return

        try:
            sim = Simulator(scenario_id, IX=ix, IY=iy, IZ=iz)
            runs = sim.simuler_40_runs()
            df_concat = pd.concat(runs, ignore_index=True)

            # Stockage du résultat dans le parent (MenuWindow)
            parent = self.parent()
            if parent is not None:
                parent.dernier_resultat_df = df_concat
                logger.debug("Résultat simulation stocké dans le parent.")

            reserve_finale = df_concat[df_concat["Annee"] == 2035]["Reserve"].mean()
            QMessageBox.information(self, "Simulation terminée",
                f"Simulation (40 runs) pour le scénario {scenario_id} effectuée.\n"
                f"Réserve moyenne finale (2035) : {reserve_finale:,.2f} DH\n"
                f"\nLes résultats sont disponibles dans le menu Résultats."
            )
            logger.info("Simulation terminée : réserve moyenne 2035 = %.2f DH", reserve_finale)
        except Exception as e:
            logger.error("Erreur lors de la simulation : %s", str(e))
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la simulation : {e}")

# --- Pour test seul ---
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     import sys
#     app = QApplication(sys.argv)
#     win = SimulationWindow()
#     win.show()
#     sys.exit(app.exec_())
