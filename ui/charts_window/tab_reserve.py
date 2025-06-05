from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from ui.charts_window import logger
from ui.dialogs import show_error, show_info

# ---- Import des helpers UX avancés ----
from ui.widgets.plot_helpers import (
    mpl_add_tooltips,
    mpl_add_export_button,
    mpl_add_crosshair,
    mpl_add_doubleclick_reset,
    mpl_add_legend_popup,
)

class TabReserve(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.filtered_df = self.data.copy()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("<b>Évolution de la réserve sur 11 ans</b>"))

        # --------- 1. Filtres dynamiques (Année, Simulation) ----------
        filter_layout = QHBoxLayout()
        self.year_combo = QComboBox()
        self.year_combo.addItem("Toutes années")
        if not self.data.empty:
            self.years = sorted(self.data["Annee"].unique())
            self.year_combo.addItems([str(a) for a in self.years])
        self.year_combo.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Année :"))
        filter_layout.addWidget(self.year_combo)

        # Ajout filtre simulation (optionnel si tu en as)
        self.sim_combo = QComboBox()
        self.sim_combo.addItem("Toutes simulations")
        if not self.data.empty and "Simulation" in self.data.columns:
            self.sims = sorted(self.data["Simulation"].unique())
            self.sim_combo.addItems([str(s) for s in self.sims])
        self.sim_combo.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Simulation :"))
        filter_layout.addWidget(self.sim_combo)

        # Ajout recherche texte (ex. pour filtrer une colonne si besoin)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Recherche rapide (optionnel)")
        self.search_edit.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_edit)

        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # --------- 2. Info nombre de lignes filtrées ----------
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
            "Essayez aussi : Export/Tooltips/Crosshair… (Bonus UX).</span>"
        ))

        self.setLayout(main_layout)
        self.apply_filters(initial=True)

    def apply_filters(self, initial=False):
        """Met à jour self.filtered_df selon les filtres choisis, puis refresh plot et infos."""
        df = self.data
        # Filtre Année
        year_val = self.year_combo.currentText()
        if year_val and year_val != "Toutes années":
            df = df[df["Annee"] == int(year_val)]
        # Filtre Simulation
        sim_val = self.sim_combo.currentText()
        if sim_val and sim_val != "Toutes simulations":
            df = df[df["Simulation"] == int(sim_val)]
        # Filtre Recherche
        query = self.search_edit.text().strip()
        if query:
            # Exemple : recherche sur toutes les colonnes str
            df = df[df.astype(str).apply(lambda row: query.lower() in " ".join(row).lower(), axis=1)]
        self.filtered_df = df.copy()
        self.row_count_label.setText(f"<b>Lignes affichées : {len(self.filtered_df):,} / {len(self.data):,}</b>")
        if not initial:
            self.plot_reserve()

    def plot_reserve(self):
        """Affiche le graphique de réserve à partir du DataFrame filtré."""
        self.figure.clear()
        try:
            if self.filtered_df.empty:
                self.canvas.draw()
                return

            ax = self.figure.add_subplot(111)
            reserve_par_annee = self.filtered_df.groupby("Annee")["Reserve"].mean()
            line, = ax.plot(
                reserve_par_annee.index,
                reserve_par_annee.values,
                marker='o',
                color='#2077B4',
                label='Réserve moyenne'
            )
            ax.set_title("Réserve moyenne (tous runs) par année")
            ax.set_xlabel("Année")
            ax.set_ylabel("Réserve (DH)")
            ax.grid(True)
            ax.legend()
            self.canvas.draw()
            logger.info("TabReserve : graphique réserve affiché (années : %s)", list(reserve_par_annee.index))

            # === BONUS PRO: helpers UX avancés ===
            mpl_add_tooltips(self.figure, ax, x=reserve_par_annee.index, y=reserve_par_annee.values, labels=[
                f"Année {a} : {v:,.0f} DH" for a, v in zip(reserve_par_annee.index, reserve_par_annee.values)
            ])
            mpl_add_export_button(self.figure, self.canvas, filename_default="reserve.png")
            mpl_add_crosshair(self.figure, ax)
            orig_xlim = ax.get_xlim()
            orig_ylim = ax.get_ylim()
            mpl_add_doubleclick_reset(self.figure, ax, orig_xlim, orig_ylim)
            mpl_add_legend_popup(self.figure, ax)
            self.canvas.mpl_connect("pick_event", self.on_pick)
            line.set_picker(5)
        except Exception as e:
            logger.error("Erreur TabReserve : %s", str(e))
            show_error(self, "Erreur graphique", f"Erreur lors de l'affichage du graphique :\n{e}")

    def on_pick(self, event):
        """Callback d’infos lors d’un clic/survol d’un point (bonus)."""
        artist = event.artist
        if hasattr(artist, "get_xdata") and hasattr(artist, "get_ydata"):
            ind = event.ind[0] if event.ind else None
            if ind is not None:
                x = artist.get_xdata()[ind]
                y = artist.get_ydata()[ind]
                show_info(self, f"<b>Année :</b> {x}<br><b>Réserve :</b> {y:,.0f} DH")

    def save_graphic(self):
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
            show_info(self, "Succès", f"Graphique sauvegardé :\n{path}")
            logger.info("TabReserve : graphique sauvegardé : %s", path)
        except Exception as e:
            logger.error("Erreur sauvegarde graphique TabReserve : %s", str(e))
            show_error(self, "Erreur", f"Erreur lors de la sauvegarde :\n{str(e)}")

    def export_filtered_df(self):
        """Exporte le DataFrame filtré en CSV."""
        if self.filtered_df.empty:
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
            self.filtered_df.to_csv(path, index=False)
            show_info(self, "Export réussi", f"Fichier CSV exporté :\n{path}")
            logger.info("TabReserve : vue filtrée exportée : %s", path)
        except Exception as e:
            logger.error("Erreur export vue filtrée TabReserve : %s", str(e))
            show_error(self, "Erreur", f"Erreur lors de l'export :\n{str(e)}")

    # ==== NEW: For PDF/report integration ====

    def get_figure(self):
        """Return the current matplotlib Figure (for PDF/report export)."""
        return self.figure

    def get_stats(self):
        """Return summary stats as a dict (for PDF/report export)."""
        if self.filtered_df.empty:
            return {}
        # Stats on filtered data
        reserve = self.filtered_df["Reserve"]
        stats = {
            "Années couvertes": sorted(self.filtered_df["Annee"].unique()),
            "Simulation(s)": sorted(self.filtered_df["Simulation"].unique()) if "Simulation" in self.filtered_df.columns else None,
            "Réserve Moyenne": float(reserve.mean()),
            "Réserve Min": float(reserve.min()),
            "Réserve Max": float(reserve.max()),
            "Nb lignes": int(len(self.filtered_df))
        }
        return stats

    def get_summary(self):
        """Return a formatted summary string of the current filtered DataFrame."""
        stats = self.get_stats()
        if not stats:
            return "Aucune donnée à résumer."
        lines = [
            f"Années couvertes : {stats['Années couvertes']}",
            f"Simulation(s) : {stats['Simulation(s)']}",
            f"Réserve Moyenne : {stats['Réserve Moyenne']:,.2f} DH",
            f"Réserve Min : {stats['Réserve Min']:,.2f} DH",
            f"Réserve Max : {stats['Réserve Max']:,.2f} DH",
            f"Nombre de lignes affichées : {stats['Nb lignes']}"
        ]
        return "\n".join(lines)

