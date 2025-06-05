from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QShortcut, QApplication
)
from PyQt5.QtGui import QKeySequence  # ✅ BON
import pandas as pd
from utils.fileio import export_dataframe_to_csv
from ui.results_window.logger import logger

class TabCSVExport(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Exporter les résultats au format CSV</b>"))

        # 1. Create and fill the table widget
        self.table = QTableWidget()
        if isinstance(self.data, pd.DataFrame):
            self._populate_table(self.data)
        layout.addWidget(self.table)

        # 2. Add copy/paste shortcuts for the table
        QShortcut(QKeySequence("Ctrl+C"), self.table, activated=self.copy_selected)
        QShortcut(QKeySequence("Ctrl+V"), self.table, activated=self.paste_selected)

        # 3. Export button
        btn = QPushButton("Exporter en CSV")
        btn.clicked.connect(self.exporter)
        layout.addWidget(btn)

    def _populate_table(self, df):
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i, row in enumerate(df.values):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def copy_selected(self):
        # Copies selected cells to clipboard as CSV
        selection = self.table.selectedRanges()
        if not selection:
            return
        s = ''
        for r in selection:
            for row in range(r.topRow(), r.bottomRow() + 1):
                row_data = []
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                s += '\t'.join(row_data) + '\n'
        QApplication.clipboard().setText(s)

    def paste_selected(self):
        # Pastes clipboard content into the selected area
        selection = self.table.selectedRanges()
        if not selection:
            return
        start_row = selection[0].topRow()
        start_col = selection[0].leftColumn()
        clipboard = QApplication.clipboard().text()
        rows = clipboard.split('\n')
        for i, row_data in enumerate(rows):
            if not row_data.strip():
                continue
            values = row_data.split('\t')
            for j, value in enumerate(values):
                r, c = start_row + i, start_col + j
                if r < self.table.rowCount() and c < self.table.columnCount():
                    self.table.setItem(r, c, QTableWidgetItem(value))

    def exporter(self):
        if self.data is None or not isinstance(self.data, pd.DataFrame):
            QMessageBox.warning(self, "Erreur", "Aucune donnée à exporter.")
            logger.warning("TabCSVExport : tentative d'export sans données.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier CSV", "resultats.csv", "CSV files (*.csv)")
        if path:
            if export_dataframe_to_csv(self.data, path):
                QMessageBox.information(self, "Succès", f"Fichier exporté :\n{path}")
                logger.info("Export CSV réussi : %s", path)
            else:
                QMessageBox.warning(self, "Erreur", "L'export a échoué.")
                logger.error("Export CSV échoué pour %s", path)
