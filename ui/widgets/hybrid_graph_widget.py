from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import pyqtgraph as pg
import pandas as pd

from ui.theme import MPL_COLORS, get_custom_palette, get_dark_palette
from utils.mpl_theme import set_mpl_theme

class HybridGraphWidget(QWidget):
    def __init__(self, data=None, engine="mpl", dark_mode=False, parent=None):
        super().__init__(parent)
        self.engine = engine      # "mpl" or "pg"
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.dark_mode = dark_mode
        self._graph_widget = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.draw_graph()

    def set_engine(self, engine):
        """Change le moteur de rendu graphique (matplotlib / pyqtgraph)."""
        if engine == self.engine:
            return
        self.engine = engine
        self.draw_graph()

    def set_data(self, data):
        """Recharge les données et redessine le graphique actif."""
        self.data = data if isinstance(data, pd.DataFrame) else pd.DataFrame()
        self.draw_graph()

    def set_dark_mode(self, dark):
        """Réapplique le thème (matplotlib/pyqtgraph) sur le graphique actif."""
        self.dark_mode = dark
        self.draw_graph()

    def clear_graph(self):
        if self._graph_widget is not None:
            self.layout.removeWidget(self._graph_widget)
            self._graph_widget.setParent(None)
            self._graph_widget.deleteLater()
            self._graph_widget = None

    def draw_graph(self):
        """Crée le widget graphique selon le moteur/les données/le thème."""
        self.clear_graph()
        if self.engine == "mpl":
            self._graph_widget = self._plot_mpl()
        else:
            self._graph_widget = self._plot_pg()
        self.layout.addWidget(self._graph_widget)

    def _plot_mpl(self):
        """Affiche la courbe (matplotlib). Zoom/pan inclus nativement."""
        set_mpl_theme(self.dark_mode)
        fig, ax = plt.subplots(figsize=(7, 4), tight_layout=True)
        if not self.data.empty and "Annee" in self.data.columns and "Reserve" in self.data.columns:
            reserve_par_annee = self.data.groupby("Annee")["Reserve"].mean()
            ax.plot(
                reserve_par_annee.index,
                reserve_par_annee.values,
                marker='o',
                color=MPL_COLORS['reserve'],
                label="Réserve moyenne"
            )
            ax.set_title("Réserve moyenne par année")
            ax.set_xlabel("Année")
            ax.set_ylabel("Réserve (DH)")
            ax.legend()
            ax.grid(True)
        else:
            ax.text(0.5, 0.5, "Aucune donnée à afficher", ha='center', va='center', fontsize=12, color="red")
        canvas = FigureCanvas(fig)
        canvas.setFocusPolicy(Qt.ClickFocus)
        canvas.setFocus()
        return canvas

    def _plot_pg(self):
        """Affiche la courbe (pyqtgraph) avec zoom/pan très fluide."""
        plt = pg.PlotWidget()
        plt.showGrid(x=True, y=True, alpha=0.4)
        if not self.data.empty and "Annee" in self.data.columns and "Reserve" in self.data.columns:
            reserve_par_annee = self.data.groupby("Annee")["Reserve"].mean()
            x = list(reserve_par_annee.index)
            y = list(reserve_par_annee.values)
            color = MPL_COLORS['reserve'] if not self.dark_mode else "#4ec8e6"
            pen = pg.mkPen(color=color, width=3)
            symbolBrush = pg.mkBrush(color)
            plt.plot(x, y, pen=pen, symbol='o', symbolBrush=symbolBrush, name="Réserve moyenne")
            plt.setTitle("Réserve moyenne par année", color="w" if self.dark_mode else "#222", size="16pt")
            plt.setLabel("bottom", "Année", color="w" if self.dark_mode else "#222", size="11pt")
            plt.setLabel("left", "Réserve (DH)", color="w" if self.dark_mode else "#222", size="11pt")
        else:
            txt = pg.TextItem("Aucune donnée à afficher", color="r", anchor=(0.5, 0.5))
            plt.addItem(txt)
        if self.dark_mode:
            plt.setBackground("#181C20")
        else:
            plt.setBackground("w")
        return plt

    # ---- Optionnel: expose le widget courant pour manip custom (zoom, tooltips…) ----
    def current_widget(self):
        return self._graph_widget

    # ---- (Bonus) Ajoute une méthode pour sélectionner engine via bouton ----
    def toggle_engine(self):
        """Bascule entre Matplotlib et PyQtGraph."""
        self.set_engine("pg" if self.engine == "mpl" else "mpl")
