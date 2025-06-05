from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from ui.charts_window import logger
from ui.dialogs import show_error, show_info
from ui.widgets.plot_helpers import (
    mpl_add_tooltips, mpl_add_export_button, mpl_add_crosshair,
    mpl_add_brush_zoom, mpl_add_doubleclick_reset, mpl_add_context_menu
)
from ui.charts_window.scenario_selector import ScenarioSelector

class TabComparaison(QWidget):
    def __init__(self, data_scenarios=None):
        super().__init__()
        self.data_scenarios = data_scenarios or {}
        self._original_xlim = None
        self._original_ylim = None

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<b>Comparaison multi-scénarios (réserve)</b>"))

        # --------- 1. Sélecteur de scénarios UX++ ----------
        self.selector = ScenarioSelector(
            scenario_names=list(self.data_scenarios.keys()),
            default_selected=list(self.data_scenarios.keys())
        )
        self.selector.selection_changed.connect(self.on_selection_changed)
        main_layout.addWidget(self.selector)

        # --------- 2. Filtres additionnels (année, recherche) ----------
        filter_layout = QHBoxLayout()
        # Année (optionnel)
        self.year_combo = QComboBox()
        self.year_combo.addItem("Toutes années")
        self._populate_years_combo()
        self.year_combo.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Année :"))
        filter_layout.addWidget(self.year_combo)

        # Recherche texte
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche rapide (optionnel)")
        self.search_edit.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_edit)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # --------- 3. Info nombre de points ----------
        self.row_count_label = QLabel()
        main_layout.addWidget(self.row_count_label)

        # --------- 4. Figure matplotlib ---------
        self.figure = Figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # --------- 5. Boutons export graphique ET vue filtrée ----------
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Enregistrer le graphique")
        self.save_btn.clicked.connect(self.save_graphic)
        btn_layout.addWidget(self.save_btn)

        self.export_df_btn = QPushButton("Exporter la vue filtrée (CSV)")
        self.export_df_btn.clicked.connect(self.export_filtered_df)
        btn_layout.addWidget(self.export_df_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # --------- 6. Astuce UX ---------
        main_layout.addWidget(QLabel(
            "<span style='color:#888;'>Astuce : Sélectionnez un ou plusieurs scénarios à comparer. "
            "Utilisez la barre Matplotlib ci-dessous pour zoomer/déplacer/pan. "
            "Double-clic ou bouton 'home' pour reset.<br/>"
            "Essayez aussi : Export, Tooltips, Crosshair, Menu contextuel… (UX Bonus).</span>"
        ))

        self.setLayout(main_layout)
        # Valeur courante du filtre scénarios (par défaut tout sélectionné)
        self.active_scenarios = set(self.data_scenarios.keys())
        self.filtered_scenarios = {k: v.copy() for k, v in self.data_scenarios.items() if k in self.active_scenarios}
        self.apply_filters(initial=True)

    def _populate_years_combo(self):
        """Mets à jour les années (intersection de toutes les années de tous les scénarios)."""
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
        """Callback quand l'utilisateur modifie la sélection de scénarios."""
        self.active_scenarios = set(selected_scenarios)
        self._populate_years_combo()
        self.apply_filters()

    def apply_filters(self, initial=False):
        """Met à jour self.filtered_scenarios selon les filtres actifs, puis refresh plot et infos."""
        year_filter = self.year_combo.currentText()
        query = self.search_edit.text().strip()

        filtered = {}
        total_points = 0
        for name in self.active_scenarios:
            df = self.data_scenarios.get(name)
            if not isinstance(df, pd.DataFrame) or df.empty:
                continue
            dff = df.copy()
            # Filtre année
            if year_filter != "Toutes années":
                dff = dff[dff["Annee"] == int(year_filter)]
            # Recherche texte
            if query:
                dff = dff[dff.astype(str).apply(lambda row: query.lower() in " ".join(row).lower(), axis=1)]
            if not dff.empty:
                filtered[name] = dff
                total_points += len(dff)
        self.filtered_scenarios = filtered
        self.row_count_label.setText(f"<b>Lignes affichées : {total_points:,}</b>")
        if not initial:
            self.plot_comparaison()
        else:
            self.plot_comparaison()  # Toujours initial pour affichage immédiat

    def plot_comparaison(self):
        """Affiche la comparaison des réserves moyennes par année et par scénario."""
        self.figure.clear()
        try:
            ax = self.figure.add_subplot(111)
            all_x, all_y, all_labels = [], [], []

            # Palette Matplotlib automatique pour n courbes/scénarios
            import matplotlib.pyplot as plt
            palette = plt.cm.get_cmap('tab10', max(3, len(self.filtered_scenarios)))
            colors = [palette(i) for i in range(len(self.filtered_scenarios))]

            for i, (nom, df) in enumerate(self.filtered_scenarios.items()):
                if df is None or df.empty:
                    continue
                reserve_par_annee = df.groupby("Annee")["Reserve"].mean()
                x = np.array(reserve_par_annee.index)
                y = np.array(reserve_par_annee.values)
                color = colors[i] if i < len(colors) else None
                ax.plot(x, y, marker='o', label=nom, color=color)
                all_x.extend(x)
                all_y.extend(y)
                all_labels.extend([f"{nom}: {a} → {v:,.0f} DH" for a, v in zip(x, y)])

            ax.set_title("Réserve moyenne par année pour chaque scénario")
            ax.set_xlabel("Année")
            ax.set_ylabel("Réserve (DH)")
            ax.grid(True)
            ax.legend()

            # --- UX Bonus Matplotlib ---
            if all_x and all_y:
                mpl_add_tooltips(self.figure, ax, np.array(all_x), np.array(all_y), labels=all_labels)
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
                mpl_add_export_button(self.figure, self.canvas, filename_default="comparaison.png")

            self.canvas.draw()
            logger.info("TabComparaison : graphique comparatif affiché (scénarios : %d, points : %d).",
                        len(self.filtered_scenarios), sum(len(df) for df in self.filtered_scenarios.values()))
        except Exception as e:
            logger.error("Erreur TabComparaison : %s", str(e))
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
            logger.info("TabComparaison : graphique sauvegardé : %s", path)
        except Exception as e:
            logger.error("Erreur sauvegarde graphique TabComparaison : %s", str(e))
            show_error(self, "Erreur", f"Erreur lors de la sauvegarde :\n{str(e)}")

    def export_filtered_df(self):
        """Exporte tous les DataFrames filtrés en CSV, concaténés."""
        if not self.filtered_scenarios or not any(len(df) for df in self.filtered_scenarios.values()):
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
            concat_df = pd.concat(self.filtered_scenarios.values())
            concat_df.to_csv(path, index=False)
            show_info(self, "Export réussi", f"Fichier CSV exporté :\n{path}")
            logger.info("TabComparaison : vue filtrée exportée : %s", path)
        except Exception as e:
            logger.error("Erreur export vue filtrée TabComparaison : %s", str(e))
            show_error(self, "Erreur", f"Erreur lors de l'export :\n{str(e)}")

    # === NEW: For PDF/report integration ===

    def get_figure(self):
        """Return the current matplotlib Figure (for PDF/report export)."""
        return self.figure

    def get_stats(self):
        """Return summary stats per scenario and global, as a dict."""
        stats = {}
        total_points = 0
        for scen, df in self.filtered_scenarios.items():
            if df.empty:
                continue
            reserve = df["Reserve"]
            stats[scen] = {
                "Années couvertes": sorted(df["Annee"].unique()),
                "Nb simulations": len(df["Simulation"].unique()) if "Simulation" in df.columns else None,
                "Réserve Moyenne": float(reserve.mean()),
                "Réserve Min": float(reserve.min()),
                "Réserve Max": float(reserve.max()),
                "Nb lignes": int(len(df)),
            }
            total_points += len(df)
        stats["__total__"] = {
            "Nombre de scénarios": len(self.filtered_scenarios),
            "Total lignes": total_points,
        }
        return stats

    def get_summary(self):
        """Return a formatted summary string of all selected scenarios."""
        stats = self.get_stats()
        if not stats or len(stats) <= 1:  # Only __total__ or empty
            return "Aucune donnée à résumer."
        lines = []
        for scen, scen_stats in stats.items():
            if scen == "__total__":
                continue
            lines.append(f"--- Scénario : {scen} ---")
            lines.append(f"  Années couvertes : {scen_stats['Années couvertes']}")
            lines.append(f"  Nombre de simulations : {scen_stats['Nb simulations']}")
            lines.append(f"  Réserve Moyenne : {scen_stats['Réserve Moyenne']:,.2f} DH")
            lines.append(f"  Réserve Min : {scen_stats['Réserve Min']:,.2f} DH")
            lines.append(f"  Réserve Max : {scen_stats['Réserve Max']:,.2f} DH")
            lines.append(f"  Nombre de lignes : {scen_stats['Nb lignes']}\n")
        if "__total__" in stats:
            total = stats["__total__"]
            lines.append(f"--- Total scénarios affichés : {total['Nombre de scénarios']}, total lignes : {total['Total lignes']:,}")
        return "\n".join(lines)
