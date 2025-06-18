from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
)
import pandas as pd

from ui.csv_import_window.tab_summary import TabSummary
from ui.csv_import_window.tab_by_year import TabByYear
from ui.csv_import_window.tab_by_year_filtered import TabByYearFiltered
from ui.csv_import_window.tab_interactive import TabCSVInteractive
from ui.widgets.fade_tab_widget import FadeTabWidget
from ui.csv_import_window.logger import logger

class CSVImportWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Résultats depuis un fichier CSV")
        self.setGeometry(280, 280, 1000, 680)

        self.data = None
        self.tabs = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.load_button = QPushButton("📂 Importer un fichier CSV")
        self.load_button.clicked.connect(self.import_csv)

        layout.addWidget(self.load_button)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)

            if not {"Annee", "Simulation"}.issubset(df.columns):
                QMessageBox.warning(self, "Colonnes manquantes",
                    "Le fichier doit contenir les colonnes 'Annee' et 'Simulation'.")
                return

            self.data = df
            logger.info("CSV importé avec succès : %s", file_path)
            self.show_tabs()

            # ✅ Mise à jour de MenuWindow si parent() est défini
            parent = self.parent()
            if parent and hasattr(parent, "set_dernier_resultat_df"):
                parent.set_dernier_resultat_df(df)
                logger.debug("Résultat CSV stocké dans MenuWindow via set_dernier_resultat_df().")

        except Exception as e:
            QMessageBox.critical(self, "Erreur d'import", f"Impossible de lire le fichier : {e}")
            logger.error("Erreur lors de l'import CSV : %s", str(e))

    def show_tabs(self):
        if self.tabs:
            self.tabs.setParent(None)

        self.tabs = FadeTabWidget()
        self.tabs.addTab(TabSummary(self.data), "📊 Résumé")
        self.tabs.addTab(TabByYear(self.data), "📆 Annuel (moyennes)")
        self.tabs.addTab(TabByYearFiltered(self.data), "🔍 Filtres dynamiques")
        self.tabs.addTab(TabCSVInteractive(self.data), "🧾 CSV interactif")

        self.centralWidget().layout().addWidget(self.tabs)
        self.tabs.setCurrentIndex(0)
        self.tabs.show()
        self.tabs.repaint()
        self.tabs.update()
        self.update()
        self.show()
