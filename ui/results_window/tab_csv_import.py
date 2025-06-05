# ui/results_window/tab_csv_import.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMessageBox
)
import pandas as pd

from ui.widgets.csv_table_widget import CSVTableWidget
from ui.widgets.sort_dialog import SortDialog
from utils.csv_sort_utils import save_sort_config, load_sort_config
from ui.results_window.logger import logger  # ✅ Ajout du logger

class TabCSVImport(QWidget):
    CONFIG_SORT_PATH = "data/config/tab_csv_import_sort.json"

    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.filtered_data = self.data.copy()
        self.max_rows_per_page = 50
        self.current_page = 0
        self.sort_columns, self.sort_orders = load_sort_config(self.CONFIG_SORT_PATH)
        self.setup_ui()
        self.apply_sort()  # Trie initial
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Import et manipulation du CSV (tri, copier/coller, pagination)</b>"))

        btn_layout = QHBoxLayout()
        self.btn_sort = QPushButton("Trier…")
        self.btn_sort.clicked.connect(self.open_sort_dialog)
        btn_layout.addWidget(self.btn_sort)

        self.btn_reset_sort = QPushButton("Réinitialiser tri")
        self.btn_reset_sort.clicked.connect(self.reset_sort)
        btn_layout.addWidget(self.btn_reset_sort)

        self.btn_copy = QPushButton("Copier (Excel)")
        self.btn_copy.clicked.connect(self.copy_selected)
        btn_layout.addWidget(self.btn_copy)

        self.btn_paste = QPushButton("Coller (Excel)")
        self.btn_paste.clicked.connect(self.paste_selected)
        btn_layout.addWidget(self.btn_paste)

        layout.addLayout(btn_layout)

        self.table = CSVTableWidget()
        layout.addWidget(self.table)

        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("← Précédent")
        self.btn_prev.clicked.connect(self.prev_page)
        nav_layout.addWidget(self.btn_prev)
        self.btn_next = QPushButton("Suivant →")
        self.btn_next.clicked.connect(self.next_page)
        nav_layout.addWidget(self.btn_next)
        self.lbl_page = QLabel()
        nav_layout.addWidget(self.lbl_page)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)

        self.setLayout(layout)

    def refresh_table(self):
        """Affiche le DataFrame trié/filtré page courante dans la table."""
        df = self.filtered_data
        n_rows = len(df)
        if n_rows == 0:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.lbl_page.setText("Aucune donnée")
            return

        start = self.current_page * self.max_rows_per_page
        end = min(start + self.max_rows_per_page, n_rows)
        sub_df = df.iloc[start:end]
        self.table.set_dataframe(sub_df)
        self.lbl_page.setText(f"Lignes {start+1}-{end} sur {n_rows} (Page {self.current_page+1}/{(n_rows-1)//self.max_rows_per_page+1})")
        logger.info("TabCSVImport : page %d affichée (%d lignes)", self.current_page + 1, len(sub_df))

    def open_sort_dialog(self):
        if self.data.empty:
            QMessageBox.information(self, "Alerte", "Aucune donnée à trier.")
            return
        dlg = SortDialog(list(self.data.columns), self)
        if dlg.exec_():
            by, asc = dlg.get_result()
            if by:
                self.sort_columns = by
                self.sort_orders = asc
                save_sort_config(self.CONFIG_SORT_PATH, self.sort_columns, self.sort_orders)
                self.apply_sort()
                self.refresh_table()
                logger.info("Tri appliqué sur colonnes %s (%s)", by, asc)

    def reset_sort(self):
        self.sort_columns, self.sort_orders = [], []
        save_sort_config(self.CONFIG_SORT_PATH, self.sort_columns, self.sort_orders)
        self.apply_sort()
        self.refresh_table()
        logger.info("Tri réinitialisé dans TabCSVImport")

    def apply_sort(self):
        if self.sort_columns:
            self.filtered_data = self.data.sort_values(
                by=self.sort_columns,
                ascending=self.sort_orders if self.sort_orders else True
            )
        else:
            self.filtered_data = self.data.copy()
        self.current_page = 0

    def next_page(self):
        max_page = max(0, (len(self.filtered_data)-1)//self.max_rows_per_page)
        if self.current_page < max_page:
            self.current_page += 1
            self.refresh_table()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_table()

    def copy_selected(self):
        self.table.copy_selected()

    def paste_selected(self):
        self.table.paste_selected()
        logger.info("Collage de contenu dans table TabCSVImport")