from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
import pandas as pd
from ui.results_window import logger

class TabByYear(QWidget):
    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Résultats annuels moyens (toutes simulations)</b>"))

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.show_table(data)

    def show_table(self, data):
        if data is None or not isinstance(data, pd.DataFrame):
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            logger.warning("TabByYear : pas de données à afficher.")
            return

        # Moyenne par année de tous les indicateurs
        try:
            df_year = data.groupby("Annee").mean().reset_index()
            cols = list(df_year.columns)
            self.table.setColumnCount(len(cols))
            self.table.setRowCount(len(df_year))
            self.table.setHorizontalHeaderLabels(cols)

            for i, row in df_year.iterrows():
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(int(val)) if isinstance(val, float) else str(val)))
            logger.info("TabByYear : tableau annuel affiché (n années = %d).", len(df_year))
        except Exception as e:
            logger.error("Erreur TabByYear : %s", str(e))
