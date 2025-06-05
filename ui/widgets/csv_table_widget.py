# ui/widgets/csv_table_widget.py

from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QAbstractItemView, QApplication,
    QVBoxLayout, QPushButton, QWidget, QFileDialog, QHBoxLayout, QShortcut, QKeySequence
)
from PyQt5.QtCore import Qt
import pandas as pd

class CSVTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget(self)
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)

        # --- Boutons Export + Copier ---
        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("Exporter la vue affichée (CSV)")
        self.export_btn.clicked.connect(self.export_current_view)
        btn_layout.addWidget(self.export_btn)

        self.copy_btn = QPushButton("Copier sélection")
        self.copy_btn.clicked.connect(self.copy_selected)
        btn_layout.addWidget(self.copy_btn)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # === 🎹 Raccourcis clavier natifs (Excel-like) ===
        QShortcut(QKeySequence("Ctrl+C"), self.table, activated=self.copy_selected)
        QShortcut(QKeySequence("Ctrl+V"), self.table, activated=self.paste_selected)

    def set_dataframe(self, df: pd.DataFrame):
        """Affiche dynamiquement le DataFrame dans la table."""
        self.table.clear()
        if df is None or df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels([str(c) for c in df.columns])
        for i, row in enumerate(df.values):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def export_current_view(self):
        """Exporte la table affichée (vue filtrée) en CSV."""
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()
        if row_count == 0 or col_count == 0:
            return
        # Récupère les données de la table (vue affichée)
        data = []
        for i in range(row_count):
            row = []
            for j in range(col_count):
                item = self.table.item(i, j)
                row.append(item.text() if item else "")
            data.append(row)
        columns = [self.table.horizontalHeaderItem(j).text() for j in range(col_count)]
        df = pd.DataFrame(data, columns=columns)
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter la vue affichée",
            "",
            "CSV (*.csv);;Tous les fichiers (*)"
        )
        if not path:
            return
        try:
            df.to_csv(path, index=False)
            from ui.dialogs import show_info
            show_info(self, "Export réussi", f"Fichier CSV exporté :\n{path}")
        except Exception as e:
            from ui.dialogs import show_error
            show_error(self, "Erreur", f"Erreur lors de l'export :\n{str(e)}")

    def copy_selected(self):
        """Copie la sélection courante dans le presse-papiers (Excel compatible)."""
        selection = self.table.selectedIndexes()
        if not selection:
            return
        rows = sorted(idx.row() for idx in selection)
        cols = sorted(idx.column() for idx in selection)
        rowcount = rows[-1] - rows[0] + 1
        colcount = cols[-1] - cols[0] + 1
        data = [[''] * colcount for _ in range(rowcount)]
        for idx in selection:
            data[idx.row() - rows[0]][idx.column() - cols[0]] = self.table.item(idx.row(), idx.column()).text()
        clipboard = '\n'.join(['\t'.join(row) for row in data])
        QApplication.clipboard().setText(clipboard)

    def paste_selected(self):
        """(Optionnel) Colle le presse-papiers sur la sélection courante."""
        clipboard = QApplication.clipboard().text()
        if not clipboard:
            return
        rows = clipboard.split('\n')
        base_row = self.table.currentRow()
        base_col = self.table.currentColumn()
        for i, row in enumerate(rows):
            cells = row.split('\t')
            for j, text in enumerate(cells):
                r = base_row + i
                c = base_col + j
                if r < self.table.rowCount() and c < self.table.columnCount():
                    self.table.setItem(r, c, QTableWidgetItem(text))
