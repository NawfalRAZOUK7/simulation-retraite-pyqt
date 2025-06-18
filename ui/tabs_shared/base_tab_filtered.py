# ui/tabs_shared/base_tab_filtered.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QPushButton, QFileDialog
)
import pandas as pd
from ui.results_window.logger import logger

class BaseTabFiltered(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.filtered_data = self.data.copy()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Résultats filtrés par année et simulation</b>"))

        # --- Filtres ---
        filter_layout = QHBoxLayout()
        self.year_combo = QComboBox()
        self.sim_combo = QComboBox()
        self.search_edit = QLineEdit()
        self.export_btn = QPushButton("Exporter la vue filtrée")
        self.export_btn.clicked.connect(self.export_filtered_view)

        self.year_combo.addItem("Toutes années")
        self.sim_combo.addItem("Toutes simulations")
        self.search_edit.setPlaceholderText("Recherche (texte)...")

        filter_layout.addWidget(QLabel("Année:"))
        filter_layout.addWidget(self.year_combo)
        filter_layout.addWidget(QLabel("Simulation:"))
        filter_layout.addWidget(self.sim_combo)
        filter_layout.addWidget(self.search_edit)
        filter_layout.addWidget(self.export_btn)
        layout.addLayout(filter_layout)

        # --- Tableau ---
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.populate_filters()
        self.update_table()

        # --- Connexions ---
        self.year_combo.currentTextChanged.connect(self.apply_filters)
        self.sim_combo.currentTextChanged.connect(self.apply_filters)
        self.search_edit.textChanged.connect(self.apply_filters)

    def populate_filters(self):
        if not isinstance(self.data, pd.DataFrame):
            return

        try:
            years = sorted(self.data["Annee"].unique())
            self.year_combo.addItems([str(y) for y in years])
            if "Simulation" in self.data.columns:
                sims = sorted(self.data["Simulation"].unique())
                self.sim_combo.addItems([str(s) for s in sims])
        except Exception as e:
            logger.error("Erreur lors du remplissage des filtres : %s", str(e))

    def apply_filters(self):
        year_text = self.year_combo.currentText()
        sim_text = self.sim_combo.currentText()
        query = self.search_edit.text().strip().lower()

        df = self.data.copy()

        if year_text != "Toutes années":
            try:
                df = df[df["Annee"] == int(year_text)]
            except Exception:
                logger.warning("Filtre année invalide : %s", year_text)

        if sim_text != "Toutes simulations" and "Simulation" in df.columns:
            try:
                df = df[df["Simulation"] == int(sim_text)]
            except Exception:
                logger.warning("Filtre simulation invalide : %s", sim_text)

        if query:
            df = df[df.astype(str).apply(lambda row: query in " ".join(row).lower(), axis=1)]

        self.filtered_data = df
        logger.debug("[BaseTabFiltered] Résultat filtré : %d lignes — Année=%s, Sim=%s, Query='%s'",
                     len(df), year_text, sim_text, query)
        self.update_table()

    def update_table(self):
        df = self.filtered_data
        self.table.clear()

        if df.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            logger.warning("BaseTabFiltered : Aucune donnée à afficher.")
            return

        df = df.reset_index(drop=True)
        cols = list(df.columns)
        self.table.setColumnCount(len(cols))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(cols)

        for i, row in df.iterrows():
            for j, val in enumerate(row):
                val_str = str(int(val)) if isinstance(val, float) else str(val)
                self.table.setItem(i, j, QTableWidgetItem(val_str))
                logger.debug("→ Cell[%d,%d] = %s", i, j, val_str)

        logger.info("BaseTabFiltered : tableau mis à jour avec %d lignes.", len(df))

    def export_filtered_view(self):
        if self.filtered_data.empty:
            logger.warning("Export CSV échoué : aucune donnée.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Exporter la vue filtrée", "", "CSV (*.csv)")
        if path:
            try:
                self.filtered_data.to_csv(path, index=False)
                logger.info("Export CSV réussi : %s", path)
            except Exception as e:
                logger.error("Erreur export CSV : %s", str(e))
