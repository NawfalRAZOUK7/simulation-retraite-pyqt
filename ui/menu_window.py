# ui/menu_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox, QApplication, QShortcut, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QColor
from ui.simulation_window import SimulationWindow
from ui.results_window.results_window import ResultsWindow
from ui.csv_import_window.csv_import_window import CSVImportWindow
from ui.charts_window.charts_window import ChartsWindow
from ui.progress_dialog import ProgressDialog
from ui.settings_window import SettingsWindow
from ui.report_window import ReportWindow  # ✅ Ajouté
from ui.widgets.animated_tool_button import AnimatedToolButton
from ui import logger

import pandas as pd
from core.simulator import Simulator

class MenuWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulation du Système de Retraite - Menu Principal")
        self.setGeometry(200, 200, 480, 500)
        self.dernier_resultat_df = None
        self.data_scenarios = None
        self.init_ui()
        self._add_shortcuts()
        logger.info("MenuWindow initialisée.")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        outer_layout = QVBoxLayout(main_widget)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(0, 45, 0, 45)

        card = QWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card.setFixedWidth(370)
        card.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #f9fafc, stop:1 #e7e9f6
            );
            border-radius: 24px;
            border: 1.2px solid #e1e6ef;
            padding: 30px 25px;
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 7)
        shadow.setColor(QColor(170, 180, 207, 70))
        card.setGraphicsEffect(shadow)

        outer_layout.addWidget(card, alignment=Qt.AlignCenter)

        title_label = QLabel("Menu Principal")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 14px;
            letter-spacing: 0.6px;
            color: #2c2f4c;
        """)
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(10)
        title_shadow.setOffset(0, 3)
        title_shadow.setColor(QColor(0, 0, 0, 50))
        title_label.setGraphicsEffect(title_shadow)
        card_layout.addWidget(title_label)

        # --- 🟡 Ancienne version (avec animation) ---
        # btn_simulation = AnimatedToolButton()
        # btn_simulation.setText("🚀 Lancer une Simulation")
        # btn_simulation.setMinimumHeight(40)

        # btn_resultats = AnimatedToolButton()
        # btn_resultats.setText("📊 Voir les Résultats")
        # btn_resultats.setMinimumHeight(40)

        # btn_graphiques = AnimatedToolButton()
        # btn_graphiques.setText("📈 Graphiques")
        # btn_graphiques.setMinimumHeight(40)

        # btn_generate_comparaison = AnimatedToolButton()
        # btn_generate_comparaison.setText("🧩 Générer comparaison multi-scénarios")
        # btn_generate_comparaison.setMinimumHeight(40)

        # btn_parametres = AnimatedToolButton()
        # btn_parametres.setText("⚙️ Paramètres")
        # btn_parametres.setMinimumHeight(40)

        # --- 🟢 Nouvelle version (sans animation, sans styles explicites) ---
        from PyQt5.QtWidgets import QPushButton

        btn_simulation = QPushButton("🚀 Lancer une Simulation")
        btn_resultats = QPushButton("📊 Voir les Résultats")
        btn_import_csv = QPushButton("📂 Importer un CSV")
        btn_graphiques = QPushButton("📈 Graphiques")
        btn_generate_comparaison = QPushButton("🧩 Générer comparaison multi-scénarios")
        btn_parametres = QPushButton("⚙️ Paramètres")
        btn_report = QPushButton("📄 Exporter rapport PDF")

        for btn in [
            btn_simulation, btn_resultats, btn_import_csv, btn_graphiques,
            btn_generate_comparaison, btn_parametres, btn_report
        ]:
            card_layout.addWidget(btn)

        btn_simulation.clicked.connect(self.ouvrir_simulation)
        btn_resultats.clicked.connect(self.ouvrir_resultats)
        btn_import_csv.clicked.connect(self.ouvrir_import_csv)
        btn_graphiques.clicked.connect(self.ouvrir_graphiques)
        btn_parametres.clicked.connect(self.ouvrir_parametres)
        btn_report.clicked.connect(self.ouvrir_fenetre_rapport)
        btn_generate_comparaison.clicked.connect(self.generer_comparaison_multi_scenarios)

        self._btn_simulation = btn_simulation
        self._btn_resultats = btn_resultats
        self._btn_import_csv = btn_import_csv
        self._btn_graphiques = btn_graphiques
        self._btn_generate_comparaison = btn_generate_comparaison
        self._btn_parametres = btn_parametres
        self._btn_report = btn_report

    def _add_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+1"), self, activated=self._btn_simulation.click)
        QShortcut(QKeySequence("Ctrl+2"), self, activated=self._btn_resultats.click)
        QShortcut(QKeySequence("Ctrl+3"), self, activated=self._btn_graphiques.click)
        QShortcut(QKeySequence("Ctrl+4"), self, activated=self._btn_generate_comparaison.click)
        QShortcut(QKeySequence("Ctrl+5"), self, activated=self._btn_parametres.click)
        QShortcut(QKeySequence("Ctrl+6"), self, activated=self._btn_import_csv.click)

    def ouvrir_simulation(self):
        self.sim_window = SimulationWindow(parent=self)
        self.sim_window.show()
        logger.info("Fenêtre Simulation ouverte.")

    def ouvrir_import_csv(self):
        self.import_window = CSVImportWindow(parent=self)
        self.import_window.show()
        logger.info("Fenêtre Import CSV ouverte.")

    def ouvrir_resultats(self):
        if self.dernier_resultat_df is not None:
            self.res_window = ResultsWindow(data=self.dernier_resultat_df)
            self.res_window.show()
            logger.info("Fenêtre Résultats ouverte.")
        else:
            QMessageBox.information(self, "Alerte", "Aucun résultat disponible. Lance une simulation d'abord.")
            logger.warning("Ouverture Résultats : pas de données disponibles.")

    def generer_comparaison_multi_scenarios(self):
        dlg = ProgressDialog("Génération multi-scénarios, veuillez patienter…", max_steps=4)
        dlg.show()
        QApplication.processEvents()

        data_scenarios = {}
        for idx, scenario_id in enumerate(range(1, 5), 1):
            sim = Simulator(scenario_id=scenario_id)  # ✅ FIX: paramètre explicite
            runs = sim.simuler_40_runs()
            df_concat = pd.concat(runs, ignore_index=True)
            nom = f"Scénario {scenario_id} – {sim.scenario.nom}"
            data_scenarios[nom] = df_concat

            dlg.set_step(idx)
            QApplication.processEvents()
            logger.info("Comparaison : scénario %s terminé (%d/4)", nom, idx)

        self.data_scenarios = data_scenarios
        dlg.close()
        QMessageBox.information(self, "Comparaison prête", "Les données multi-scénarios ont été générées avec succès.\nUtilisez maintenant le bouton 'Graphiques'.")
        logger.info("Comparaison multi-scénarios générée avec succès.")

    def ouvrir_graphiques(self):
        if self.dernier_resultat_df is None:
            QMessageBox.information(self, "Info",
                                    "Aucune donnée disponible pour les graphiques.\nImportez un CSV ou lancez une simulation.")
            logger.warning("Ouverture Graphiques : aucun résultat de simulation ou CSV.")
            return

        if self.data_scenarios is None:
            logger.info("Ouverture Graphiques : affichage simple sans comparaison.")
            self.charts_window = ChartsWindow(data=self.dernier_resultat_df, data_scenarios=None)
        else:
            logger.info("Ouverture Graphiques : affichage avec comparaison multi-scénarios.")
            self.charts_window = ChartsWindow(data=self.dernier_resultat_df, data_scenarios=self.data_scenarios)

        self.charts_window.show()

    def ouvrir_parametres(self):
        dlg = SettingsWindow(parent=self)
        dlg.exec_()
        logger.info("Fenêtre Paramètres ouverte.")

    def set_dernier_resultat_df(self, df):
        """Permet à une fenêtre fille (ex: CSVImportWindow) de définir le résultat courant."""
        self.dernier_resultat_df = df

    def ouvrir_fenetre_rapport(self):
        if self.dernier_resultat_df is None:
            QMessageBox.information(self, "Info", "Aucune donnée disponible pour générer un rapport.")
            logger.warning("Ouverture ReportWindow : aucun résultat disponible.")
            return

        dlg = ReportWindow(data=self.dernier_resultat_df, data_scenarios=self.data_scenarios, parent=self)
        dlg.exec_()  # ← meilleure UX + modal
        logger.info("Fenêtre Rapport PDF ouverte.")

# --- Pour test seul ---
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     import sys
#     app = QApplication(sys.argv)
#     win = MenuWindow()
#     win.show()
#     sys.exit(app.exec_())

