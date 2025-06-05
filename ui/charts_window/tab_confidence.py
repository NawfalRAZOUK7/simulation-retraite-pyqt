from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from utils.stats import intervalle_confiance_reserve
from ui.charts_window import logger
from ui.dialogs import show_error, show_info
from ui.widgets.plot_helpers import (
    mpl_add_tooltips, mpl_add_export_button, mpl_add_crosshair,
    mpl_add_brush_zoom, mpl_add_doubleclick_reset, mpl_add_context_menu
)

class TabConfidence(QWidget):
    def __init__(self, data=None, alpha=0.05):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.filtered_data = self.data.copy()
        self.alpha = alpha
        self._original_xlim = None
        self._original_ylim = None

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<b>Intervalle de confiance sur la réserve par année</b>"))

        # --------- 1. Filtres dynamiques ----------
        filter_layout = QHBoxLayout()
        # Filtre année
        self.year_combo = QComboBox()
        self.year_combo.addItem("Toutes années")
        self.all_years = sorted(self.data["Annee"].unique()) if not self.data.empty else []
        for a in self.all_years:
            self.year_combo.addItem(str(a))
        self.year_combo.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Année :"))
        filter_layout.addWidget(self.year_combo)

        # Filtre sur la valeur de réserve (input min)
        self.reserve_min_edit = QLineEdit()
        self.reserve_min_edit.setPlaceholderText("Réserve min (optionnel)")
        self.reserve_min_edit.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.reserve_min_edit)

        # Recherche texte (optionnel)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche rapide (optionnel)")
        self.search_edit.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_edit)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # --------- 2. Info nombre de points ----------
        self.row_count_label = QLabel()
        main_layout.addWidget(self.row_count_label)

        # --------- 3. Figure matplotlib ---------
        self.figure = Figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # --------- 4. Boutons export graphique ET vue filtrée ----------
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Enregistrer le graphique")
        self.save_btn.clicked.connect(self.save_graphic)
        btn_layout.addWidget(self.save_btn)

        self.export_df_btn = QPushButton("Exporter la vue filtrée (CSV)")
        self.export_df_btn.clicked.connect(self.export_filtered_df)
        btn_layout.addWidget(self.export_df_btn)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # --------- 5. Astuce UX ---------
        main_layout.addWidget(QLabel(
            "<span style='color:#888;'>Astuce : Utilisez la barre Matplotlib ci-dessous pour zoomer/déplacer/pan. "
            "Double-clic ou bouton 'home' pour reset.<br/>"
            "Essayez aussi : Export, Tooltips, Crosshair, Menu contextuel… (UX Bonus).</span>"
        ))

        self.setLayout(main_layout)
        self.apply_filters(initial=True)

    def apply_filters(self, initial=False):
        year_filter = self.year_combo.currentText()
        reserve_min_text = self.reserve_min_edit.text().strip()
        query = self.search_edit.text().strip()

        filtered = self.data.copy()
        # Filtre année
        if year_filter != "Toutes années":
            filtered = filtered[filtered["Annee"] == int(year_filter)]
        # Filtre min réserve
        if reserve_min_text:
            try:
                val = float(reserve_min_text)
                filtered = filtered[filtered["Reserve"] >= val]
            except ValueError:
                pass
        # Recherche texte
        if query:
            filtered = filtered[filtered.astype(str).apply(lambda row: query.lower() in " ".join(row).lower(), axis=1)]

        self.filtered_data = filtered
        self.row_count_label.setText(f"<b>Lignes affichées : {len(filtered):,}</b>")
        if not initial:
            self.plot_confidence()

    def plot_confidence(self):
        """Affiche les IC annuels sous forme de barres verticales + tous les bonus UX."""
        self.figure.clear()
        try:
            if self.filtered_data.empty:
                self.canvas.draw()
                return

            annees = sorted(self.filtered_data["Annee"].unique())
            moyennes, ic_lows, ic_highs = [], [], []

            for annee in annees:
                ic_low, ic_high = intervalle_confiance_reserve(self.filtered_data, annee, alpha=self.alpha)
                reserve = self.filtered_data[self.filtered_data["Annee"] == annee]["Reserve"].mean()
                moyennes.append(reserve)
                ic_lows.append(reserve - ic_low if ic_low is not None else 0)
                ic_highs.append(ic_high - reserve if ic_high is not None else 0)

            x = np.array(annees)
            y = np.array(moyennes)
            err = np.array([ic_lows, ic_highs])

            ax = self.figure.add_subplot(111)
            # Courbe + barres d'erreur
            line = ax.errorbar(
                x, y,
                yerr=err,
                fmt='o-', color='#70AD47',
                ecolor='#C44D58', elinewidth=2, capsize=4, label='Réserve (IC 95%)'
            )
            ax.set_xlabel("Année")
            ax.set_ylabel("Réserve (DH)")
            ax.set_title("IC 95% de la réserve par année")
            ax.grid(True)
            ax.legend()

            # --- UX Bonus ---
            if len(x) > 0 and len(y) > 0:
                # Tooltips sur les points principaux
                mpl_add_tooltips(self.figure, ax, x, y,
                                 fmt="Année: {x} - Moyenne: {y} DH", precision=0)
                mpl_add_crosshair(self.figure, ax)
                mpl_add_brush_zoom(self.figure, ax)
                self._original_xlim = ax.get_xlim()
                self._original_ylim = ax.get_ylim()
                mpl_add_doubleclick_reset(self.figure, ax, self._original_xlim, self._original_ylim)
                mpl_add_context_menu(
                    self.figure, ax,
                    items=[
                        ("Exporter graphique", self.save_graphic),
                        ("Réinitialiser zoom", self.reset_zoom)
                    ]
                )
                mpl_add_export_button(self.figure, self.canvas, filename_default="confidence.png")

            self.canvas.draw()
            logger.info("TabConfidence : graphique IC affiché (années : %s)", annees)
        except Exception as e:
            logger.error("Erreur TabConfidence : %s", str(e))
            show_error(self, "Erreur graphique", f"Erreur lors de l'affichage du graphique :\n{e}")

    def reset_zoom(self):
        """Réinitialise le zoom du graphique (après brush ou zoom)."""
        try:
            ax = self.figure.axes[0]
            if self._original_xlim and self._original_ylim:
                ax.set_xlim(self._original_xlim)
                ax.set_ylim(self._original_ylim)
                self.canvas.draw_idle()
        except Exception:
            pass

    def save_graphic(self, export_only=False):
        """Ouvre un QFileDialog et sauvegarde la figure matplotlib."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le graphique",
            "",
            "PNG (*.png);;JPEG (*.jpg);;PDF (*.pdf);;SVG (*.svg);;All Files (*)"
        )
        if not path:
            return  # Annulé

        try:
            self.figure.savefig(path)
            if not export_only:
                show_info(self, "Succès", f"Graphique sauvegardé :\n{path}")
            logger.info("TabConfidence : graphique sauvegardé : %s", path)
        except Exception as e:
            logger.error("Erreur sauvegarde graphique TabConfidence : %s", str(e))
            show_error(self, "Erreur", f"Erreur lors de la sauvegarde :\n{str(e)}")

    def export_filtered_df(self):
        """Exporte le DataFrame filtré en CSV."""
        if self.filtered_data.empty:
            show_error(self, "Aucune donnée à exporter !")
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter la vue filtrée",
            "",
            "CSV (*.csv);;Tous les fichiers (*)"
        )
        if not path:
            return
        try:
            self.filtered_data.to_csv(path, index=False)
            show_info(self, "Export réussi", f"Fichier CSV exporté :\n{path}")
            logger.info("TabConfidence : vue filtrée exportée : %s", path)
        except Exception as e:
            logger.error("Erreur export vue filtrée TabConfidence : %s", str(e))
            show_error(self, "Erreur", f"Erreur lors de l'export :\n{str(e)}")

    # === NEW: For PDF/report integration ===

    def get_figure(self):
        """Return the current matplotlib Figure (for PDF/report export)."""
        return self.figure

    def get_stats(self):
        """Return summary stats as a dict (for PDF/report export)."""
        if self.filtered_data.empty:
            return {}
        reserve = self.filtered_data["Reserve"]
        stats = {
            "Années couvertes": sorted(self.filtered_data["Annee"].unique()),
            "Nb simulations": len(self.filtered_data["Simulation"].unique()) if "Simulation" in self.filtered_data.columns else None,
            "Réserve Moyenne": float(reserve.mean()),
            "Réserve Min": float(reserve.min()),
            "Réserve Max": float(reserve.max()),
            "Nb lignes": int(len(self.filtered_data)),
            "Alpha (niveau confiance)": self.alpha
        }
        return stats

    def get_summary(self):
        """Return a formatted summary string of the current filtered DataFrame."""
        stats = self.get_stats()
        if not stats:
            return "Aucune donnée à résumer."
        lines = [
            f"Années couvertes : {stats['Années couvertes']}",
            f"Nombre de simulations : {stats['Nb simulations']}",
            f"Réserve Moyenne : {stats['Réserve Moyenne']:,.2f} DH",
            f"Réserve Min : {stats['Réserve Min']:,.2f} DH",
            f"Réserve Max : {stats['Réserve Max']:,.2f} DH",
            f"Nombre de lignes affichées : {stats['Nb lignes']}",
            f"Alpha (niveau de confiance): {stats['Alpha (niveau confiance)']}"
        ]
        return "\n".join(lines)
