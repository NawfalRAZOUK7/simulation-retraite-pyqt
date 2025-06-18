from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
)
import pandas as pd
from ui.charts_window.logger import logger
from ui.dialogs import show_error, show_info
from ui.graph_window import GraphWindow  # ✅ Ajout pour la fenêtre graphique dédiée

class TabConfidence(QWidget):
    def __init__(self, data=None, alpha=0.05):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.filtered_data = self.data.copy()
        self.alpha = alpha

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<b>Intervalle de confiance sur la réserve par année</b>"))

        # --------- 1. Filtres dynamiques ----------
        filter_layout = QHBoxLayout()

        self.year_combo = QComboBox()
        self.year_combo.addItem("Toutes années")
        self.all_years = sorted(self.data["Annee"].unique()) if not self.data.empty else []
        for a in self.all_years:
            self.year_combo.addItem(str(a))
        self.year_combo.currentIndexChanged.connect(self.update_status)
        filter_layout.addWidget(QLabel("Année :"))
        filter_layout.addWidget(self.year_combo)

        self.reserve_min_edit = QLineEdit()
        self.reserve_min_edit.setPlaceholderText("Réserve min (optionnel)")
        self.reserve_min_edit.textChanged.connect(self.update_status)
        filter_layout.addWidget(self.reserve_min_edit)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche rapide (optionnel)")
        self.search_edit.textChanged.connect(self.update_status)
        filter_layout.addWidget(self.search_edit)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # --------- 2. Info nombre de points ----------
        self.row_count_label = QLabel()
        main_layout.addWidget(self.row_count_label)

        # --------- 3. Bouton Affichage Graphique ---------
        self.open_graph_btn = QPushButton("📈 Afficher le graphique IC")
        self.open_graph_btn.clicked.connect(self.open_graph)
        main_layout.addWidget(self.open_graph_btn)

        # --------- 4. Astuce UX ---------
        main_layout.addWidget(QLabel(
            "<span style='color:#888;'>Astuce : Les filtres ci-dessus seront appliqués dans une fenêtre dédiée au graphique.</span>"
        ))

        self.setLayout(main_layout)
        self.update_status()

    def _get_filtered_df(self):
        df = self.data.copy()
        # Filtre année
        year_val = self.year_combo.currentText()
        if year_val != "Toutes années":
            try:
                df = df[df["Annee"] == int(year_val)]
            except ValueError:
                pass
        # Filtre réserve min
        reserve_min_text = self.reserve_min_edit.text().strip()
        if reserve_min_text:
            try:
                val = float(reserve_min_text)
                df = df[df["Reserve"] >= val]
            except ValueError:
                pass
        # Recherche texte
        query = self.search_edit.text().strip()
        if query:
            df = df[df.astype(str).apply(lambda row: query.lower() in " ".join(row).lower(), axis=1)]
        return df

    def update_status(self):
        self.filtered_data = self._get_filtered_df()
        self.row_count_label.setText(f"<b>Lignes affichées : {len(self.filtered_data):,} / {len(self.data):,}</b>")

    def open_graph(self):
        """Ouvre une fenêtre avec le graphique IC."""
        df = self._get_filtered_df()
        if df.empty:
            show_info(self, "Aucune donnée", "Aucune donnée à afficher avec les filtres sélectionnés.")
            return

        # ✅ Ouverture dans GraphWindow
        self.graph_win = GraphWindow(
            data=df,
            title="Intervalle de Confiance Réserve",
            mode="confidence",  # Pour afficher le graphique IC
            confidence_alpha=self.alpha
        )
        self.graph_win.show()

    def update_chart(self, data: pd.DataFrame):
        """Méthode appelée depuis l’extérieur pour forcer une mise à jour."""
        if isinstance(data, pd.DataFrame):
            self.data = data.copy()
            self.all_years = sorted(self.data["Annee"].unique()) if not self.data.empty else []
            self.year_combo.clear()
            self.year_combo.addItem("Toutes années")
            for a in self.all_years:
                self.year_combo.addItem(str(a))
            self.update_status()
