# ui/tabs_shared/base_tab_interactive.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)
import pandas as pd
from ui.results_window.logger import logger

class BaseTabInteractive(QWidget):
    def __init__(self, data=None, title="Tableau interactif"):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{title}</b>"))

        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.show_table()

    def show_table(self):
        if self.data.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            logger.warning("BaseTabInteractive : Aucune donnée à afficher.")
            return

        try:
            df = self.data.reset_index(drop=True)
            cols = list(df.columns)

            self.table.setColumnCount(len(cols))
            self.table.setRowCount(len(df))
            self.table.setHorizontalHeaderLabels(cols)

            for i, row in df.iterrows():
                for j, val in enumerate(row):
                    val_str = str(int(val)) if isinstance(val, float) else str(val)
                    self.table.setItem(i, j, QTableWidgetItem(val_str))

            logger.info("BaseTabInteractive : tableau affiché avec %d lignes.", len(df))

        except Exception as e:
            logger.error("Erreur dans BaseTabInteractive : %s", str(e))
