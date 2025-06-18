from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
)
import pandas as pd
from ui.charts_window.logger import logger
from ui.graph_window import GraphWindow  # ✅ Fenêtre dédiée
from ui.charts_window.scenario_selector import ScenarioSelector
from ui.dialogs import show_info

class TabComparaison(QWidget):
    def __init__(self, data_scenarios=None):
        super().__init__()
        self.data_scenarios = data_scenarios or {}

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<b>Comparaison multi-scénarios (réserve)</b>"))

        # 1. Sélecteur de scénarios
        self.selector = ScenarioSelector(
            scenario_names=list(self.data_scenarios.keys()),
            default_selected=list(self.data_scenarios.keys())
        )
        self.selector.selection_changed.connect(self.on_selection_changed)
        main_layout.addWidget(self.selector)

        # 2. Filtres dynamiques
        filter_layout = QHBoxLayout()
        self.year_combo = QComboBox()
        self.year_combo.addItem("Toutes années")
        self._populate_years_combo()
        self.year_combo.currentIndexChanged.connect(self.update_status)
        filter_layout.addWidget(QLabel("Année :"))
        filter_layout.addWidget(self.year_combo)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche rapide (optionnel)")
        self.search_edit.textChanged.connect(self.update_status)
        filter_layout.addWidget(self.search_edit)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # 3. Infos + bouton
        self.row_count_label = QLabel()
        main_layout.addWidget(self.row_count_label)

        self.btn_open_graph = QPushButton("📊 Afficher le graphique")
        self.btn_open_graph.clicked.connect(self.ouvrir_graphique)
        main_layout.addWidget(self.btn_open_graph)

        # 4. Aide UX
        main_layout.addWidget(QLabel(
            "<span style='color:#888;'>Astuce : sélectionnez les scénarios, puis cliquez sur le bouton pour afficher le graphique dans une fenêtre dédiée.</span>"
        ))

        self.setLayout(main_layout)
        self.active_scenarios = set(self.data_scenarios.keys())
        self.update_status()

    def _populate_years_combo(self):
        self.year_combo.clear()
        self.year_combo.addItem("Toutes années")
        years = set()
        for name in self.selector.selected_scenarios():
            df = self.data_scenarios.get(name)
            if isinstance(df, pd.DataFrame) and "Annee" in df.columns:
                years.update(df["Annee"].unique())
        for y in sorted(years):
            self.year_combo.addItem(str(y))

    def on_selection_changed(self, selected_scenarios):
        self.active_scenarios = set(selected_scenarios)
        self._populate_years_combo()
        self.update_status()

    def update_status(self):
        """Met à jour le label d'information sur les lignes filtrées."""
        count = 0
        for name in self.active_scenarios:
            df = self.data_scenarios.get(name)
            if not isinstance(df, pd.DataFrame) or df.empty:
                continue
            dff = df.copy()
            if self.year_combo.currentText() != "Toutes années":
                try:
                    year = int(self.year_combo.currentText())
                    dff = dff[dff["Annee"] == year]
                except ValueError:
                    pass
            query = self.search_edit.text().strip()
            if query:
                dff = dff[dff.astype(str).apply(lambda row: query.lower() in " ".join(row), axis=1)]
            count += len(dff)
        self.row_count_label.setText(f"<b>Lignes potentiellement affichées : {count:,}</b>")

    def ouvrir_graphique(self):
        """Ouvre une fenêtre dédiée avec le graphique comparatif."""
        filtered = {}
        year_filter = self.year_combo.currentText()
        query = self.search_edit.text().strip()

        for name in self.active_scenarios:
            df = self.data_scenarios.get(name)
            if not isinstance(df, pd.DataFrame) or df.empty:
                continue
            dff = df.copy()
            if year_filter != "Toutes années":
                try:
                    year = int(year_filter)
                    dff = dff[dff["Annee"] == year]
                except ValueError:
                    pass
            if query:
                dff = dff[dff.astype(str).apply(lambda row: query.lower() in " ".join(row), axis=1)]
            if not dff.empty:
                filtered[name] = dff

        if not filtered:
            show_info(self, "Aucune donnée", "Aucun scénario ne correspond aux filtres.")
            return

        self.graph_win = GraphWindow(
            filtered,
            title="Comparaison multi-scénarios",
            y_label="Réserve (DH)",
            mode="multi"  # ✅ Important pour gérer dict de scénarios
        )
        self.graph_win.show()
