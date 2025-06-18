from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
)
import pandas as pd
from ui.charts_window.logger import logger
from ui.graph_window import GraphWindow
from ui.dialogs import show_error, show_info

class TabReserve(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.filtered_df = self.data.copy()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<b>Évolution de la réserve sur 11 ans</b>"))

        # Filtres dynamiques
        filter_layout = QHBoxLayout()

        self.year_combo = QComboBox()
        self.year_combo.addItem("Toutes années")
        if not self.data.empty:
            self.years = sorted(self.data["Annee"].unique())
            self.year_combo.addItems([str(a) for a in self.years])
        self.year_combo.currentIndexChanged.connect(self.update_status)
        filter_layout.addWidget(QLabel("Année :"))
        filter_layout.addWidget(self.year_combo)

        self.sim_combo = QComboBox()
        self.sim_combo.addItem("Toutes simulations")
        if not self.data.empty and "Simulation" in self.data.columns:
            self.sims = sorted(self.data["Simulation"].unique())
            self.sim_combo.addItems([str(s) for s in self.sims])
        self.sim_combo.currentIndexChanged.connect(self.update_status)
        filter_layout.addWidget(QLabel("Simulation :"))
        filter_layout.addWidget(self.sim_combo)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche rapide (optionnel)")
        self.search_edit.textChanged.connect(self.update_status)
        filter_layout.addWidget(self.search_edit)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Résumé lignes filtrées
        self.row_count_label = QLabel()
        main_layout.addWidget(self.row_count_label)

        # Bouton "Afficher graphique"
        self.open_graph_btn = QPushButton("📈 Afficher le graphique")
        self.open_graph_btn.clicked.connect(self.open_graph)
        main_layout.addWidget(self.open_graph_btn)

        main_layout.addWidget(QLabel(
            "<span style='color:#888;'>Astuce : Les filtres ci-dessus seront appliqués dans une fenêtre dédiée au graphique.</span>"
        ))

        self.setLayout(main_layout)
        self.update_status()

    def update_status(self):
        """Met à jour le label d’info pour montrer combien de lignes seront affichées."""
        df = self._get_filtered_df()
        self.filtered_df = df
        self.row_count_label.setText(f"<b>Lignes affichées : {len(df):,} / {len(self.data):,}</b>")

    def _get_filtered_df(self):
        """Retourne un DataFrame filtré selon les combos et recherche."""
        df = self.data.copy()
        year_val = self.year_combo.currentText()
        if year_val != "Toutes années":
            try:
                df = df[df["Annee"] == int(year_val)]
            except ValueError:
                pass
        sim_val = self.sim_combo.currentText()
        if sim_val != "Toutes simulations":
            try:
                df = df[df["Simulation"] == int(sim_val)]
            except ValueError:
                pass
        query = self.search_edit.text().strip()
        if query:
            df = df[df.astype(str).apply(lambda row: query.lower() in " ".join(row).lower(), axis=1)]
        return df

    def open_graph(self):
        """Affiche la fenêtre dédiée avec le graphique de réserve."""
        df = self._get_filtered_df()
        if df.empty:
            show_info(self, "Aucune donnée", "Aucune donnée ne correspond aux filtres sélectionnés.")
            return

        self.graph_win = GraphWindow(
            data=df,
            title="Évolution de la réserve",
            y_label="Réserve (DH)",
            mode="line"  # ✅ Spécifie le mode de tracé
        )
        self.graph_win.show()

    def update_chart(self, new_data):
        if isinstance(new_data, pd.DataFrame):
            self.data = new_data.copy()
            self.update_status()
        else:
            logger.warning("TabReserve.update_chart() a reçu un type invalide : %s", type(new_data))
