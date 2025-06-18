# ui/report_window.py

import os
import pandas as pd
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QCheckBox, QLabel, QPushButton,
    QHBoxLayout, QFileDialog, QGroupBox
)

from ui.charts_window import TabReserve, TabComparaison, TabConfidence
from ui.results_window import TabSummary, TabByYear
from ui.dialogs import show_error, confirm_export_success, confirm_export_failure
from utils.pdf_export import export_report_to_pdf


class ReportWindow(QDialog):
    def __init__(self, data: pd.DataFrame, data_scenarios: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🧾 Générer un rapport PDF de simulation")
        self.setMinimumWidth(600)

        self.data = data
        self.data_scenarios = data_scenarios or {}

        layout = QVBoxLayout(self)

        # --- Groupe: Sections globales ---
        group_global = QGroupBox("Sections globales")
        global_layout = QVBoxLayout()

        self.cb_summary = QCheckBox("Inclure le résumé général")
        self.cb_summary.setChecked(True)
        global_layout.addWidget(self.cb_summary)

        self.cb_stats = QCheckBox("Inclure les statistiques")
        self.cb_stats.setChecked(True)
        global_layout.addWidget(self.cb_stats)

        self.cb_figures = QCheckBox("Inclure les graphiques")
        self.cb_figures.setChecked(True)
        global_layout.addWidget(self.cb_figures)

        group_global.setLayout(global_layout)
        layout.addWidget(group_global)

        # --- Groupe: Onglets à inclure ---
        self.group_tabs = QGroupBox("Onglets à inclure")
        group_layout = QVBoxLayout()

        self.cb_reserve = QCheckBox("Simulation principale (Réserve sur 11 ans)")
        self.cb_comparaison = QCheckBox("Comparaison multi-scénarios")
        self.cb_confidence = QCheckBox("Intervalles de confiance")
        self.cb_tab_summary = QCheckBox("Vue Résumée par Simulation")
        self.cb_tab_by_year = QCheckBox("Vue Moyenne par Année")

        self.cb_reserve.setChecked(True)
        self.cb_comparaison.setChecked(bool(self.data_scenarios))
        self.cb_confidence.setChecked(True)
        self.cb_tab_summary.setChecked(True)
        self.cb_tab_by_year.setChecked(True)

        group_layout.addWidget(self.cb_reserve)
        group_layout.addWidget(self.cb_comparaison)
        group_layout.addWidget(self.cb_confidence)
        group_layout.addWidget(self.cb_tab_summary)
        group_layout.addWidget(self.cb_tab_by_year)

        self.group_tabs.setLayout(group_layout)
        layout.addWidget(self.group_tabs)

        # --- Bouton Export ---
        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("Exporter le rapport PDF")
        self.export_btn.clicked.connect(self.generate_pdf)
        btn_layout.addStretch()
        btn_layout.addWidget(self.export_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def generate_pdf(self):
        export_path, _ = QFileDialog.getSaveFileName(
            self, "Choisir le fichier PDF", "rapport_simulation.pdf", "PDF (*.pdf)"
        )
        if not export_path:
            return
        if not export_path.lower().endswith(".pdf"):
            export_path += ".pdf"

        try:
            tabs = []

            if self.cb_reserve.isChecked() and isinstance(self.data, pd.DataFrame):
                tabs.append(TabReserve(self.data))
            if self.cb_comparaison.isChecked() and isinstance(self.data_scenarios, dict):
                tabs.append(TabComparaison(self.data_scenarios))
            if self.cb_confidence.isChecked() and isinstance(self.data, pd.DataFrame):
                tabs.append(TabConfidence(self.data))
            if self.cb_tab_summary.isChecked() and isinstance(self.data, pd.DataFrame):
                tabs.append(TabSummary(self.data))
            if self.cb_tab_by_year.isChecked() and isinstance(self.data, pd.DataFrame):
                tabs.append(TabByYear(self.data))

            figures, stats, summary = [], [], ""

            for tab in tabs:
                # ⚠️ Forcer le rendu et les données
                if hasattr(tab, "apply_filters"):
                    tab.apply_filters(initial=True)
                elif hasattr(tab, "plot_reserve"):
                    tab.plot_reserve()
                elif hasattr(tab, "plot_comparaison"):
                    tab.plot_comparaison()
                elif hasattr(tab, "plot_confidence"):
                    tab.plot_confidence()

                if self.cb_figures.isChecked() and hasattr(tab, "get_figure"):
                    fig = tab.get_figure()
                    if fig:
                        figures.append(fig)

                if self.cb_stats.isChecked() and hasattr(tab, "get_stats"):
                    stat = tab.get_stats()
                    if stat:
                        stats.append((tab.__class__.__name__, stat))

                if self.cb_summary.isChecked() and hasattr(tab, "get_summary"):
                    s = tab.get_summary()
                    if s:
                        summary += s + "\n\n"

            sections = []
            if self.cb_summary.isChecked():
                sections.append("summary")
            if self.cb_stats.isChecked():
                sections.append("stats")
            if self.cb_figures.isChecked():
                sections.append("figures")

            ok = export_report_to_pdf(
                path=export_path,
                figures=figures,
                stats=stats,
                summary=summary.strip(),
                sections=sections,
                title="Rapport Simulation Retraite",
                author="Nawfal RAZOUK"
            )

            if ok:
                confirm_export_success(export_path, parent=self)
            else:
                confirm_export_failure(export_path, "Erreur inconnue", parent=self)

        except Exception as e:
            show_error(self, "Erreur export PDF", str(e))
