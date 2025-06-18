# ui/tabs_shared/base_tab_by_year.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
import pandas as pd
from ui.results_window.logger import logger

class BaseTabByYear(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Résultats annuels moyens (toutes simulations)</b>"))

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.show_table()

    def show_table(self):
        if self.data.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            logger.warning("BaseTabByYear : pas de données à afficher.")
            return

        try:
            df_year = self.data.groupby("Annee").mean(numeric_only=True).reset_index()
            cols = list(df_year.columns)

            self.table.setColumnCount(len(cols))
            self.table.setRowCount(len(df_year))
            self.table.setHorizontalHeaderLabels(cols)

            for i, row in df_year.iterrows():
                for j, val in enumerate(row):
                    item_text = str(int(val)) if isinstance(val, float) else str(val)
                    self.table.setItem(i, j, QTableWidgetItem(item_text))

            logger.info("BaseTabByYear : tableau annuel affiché (%d années)", len(df_year))
            self.table.repaint()
            self.table.update()
            self.repaint()
            self.update()

        except Exception as e:
            logger.error("Erreur BaseTabByYear : %s", str(e))
