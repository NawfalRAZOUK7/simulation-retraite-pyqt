import os
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.dialogs import show_error, show_info
from ui.widgets.plot_helpers import (
    mpl_add_tooltips, mpl_add_crosshair,
    mpl_add_brush_zoom, mpl_add_doubleclick_reset,
    mpl_add_context_menu, mpl_add_export_button
)

from utils.stats import intervalle_confiance_reserve

ASSETS_DIR = "assets"

class GraphWindow(QMainWindow):
    def __init__(self, data, title="Graphique", y_label="Réserve", parent=None, mode="line", confidence_alpha=0.05):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 1000, 600)
        self.data = data
        self.mode = mode  # "line", "multi", "confidence"
        self.confidence_alpha = confidence_alpha
        self._original_xlim = None
        self._original_ylim = None

        self.init_ui(title, y_label)

    def init_ui(self, title, y_label):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.figure = Figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Enregistrer l'image")
        self.save_btn.clicked.connect(self.save_graphic)
        button_layout.addWidget(self.save_btn)

        self.export_btn = QPushButton("🧾 Exporter en CSV")
        self.export_btn.clicked.connect(self.export_csv)
        button_layout.addWidget(self.export_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.plot(title, y_label)

    def plot(self, title, y_label):
        self.figure.clear()
        try:
            ax = self.figure.add_subplot(111)
            all_x, all_y, all_labels = [], [], []

            if self.mode == "multi" and isinstance(self.data, dict):
                import matplotlib.pyplot as plt
                palette = plt.cm.get_cmap('tab10', max(3, len(self.data)))
                colors = [palette(i) for i in range(len(self.data))]

                for i, (label, df) in enumerate(self.data.items()):
                    if df.empty:
                        continue
                    reserve_par_annee = df.groupby("Annee")["Reserve"].mean()
                    x = np.array(reserve_par_annee.index, dtype=int)
                    y = np.array(reserve_par_annee.values)
                    ax.plot(x, y, marker='o', label=label, color=colors[i])
                    all_x.extend(x)
                    all_y.extend(y)
                    all_labels.extend([f"{label} — {a}: {v:,.0f} DH" for a, v in zip(x, y)])

            elif self.mode == "confidence" and isinstance(self.data, pd.DataFrame):
                df = self.data.copy()
                x_vals = sorted(df["Annee"].unique())
                means, ic_lows, ic_highs = [], [], []

                for year in x_vals:
                    mean = df[df["Annee"] == year]["Reserve"].mean()
                    low, high = intervalle_confiance_reserve(df, year, alpha=self.confidence_alpha)
                    means.append(mean)
                    ic_lows.append(mean - low if low is not None else 0)
                    ic_highs.append(high - mean if high is not None else 0)

                x = np.array(x_vals, dtype=int)
                y = np.array(means)
                err = np.array([ic_lows, ic_highs])

                ax.errorbar(
                    x, y, yerr=err,
                    fmt='o-', color='#70AD47',
                    ecolor='#C44D58', capsize=4,
                    label="Réserve (IC)"
                )
                all_x, all_y = x, y
                all_labels = [f"Année {a}: {v:,.0f} DH" for a, v in zip(x, y)]

            elif isinstance(self.data, pd.DataFrame):
                reserve_par_annee = self.data.groupby("Annee")["Reserve"].mean()
                x = np.array(reserve_par_annee.index, dtype=int)
                y = np.array(reserve_par_annee.values)
                ax.plot(x, y, marker='o', color="#0077cc", label="Réserve moyenne")
                all_x, all_y = x, y
                all_labels = [f"Année {a}: {v:,.0f} DH" for a, v in zip(x, y)]

            else:
                raise ValueError("Format ou mode de données non pris en charge.")

            ax.set_title(title)
            ax.set_xlabel("Année")
            ax.set_ylabel(y_label)
            ax.grid(True)
            ax.legend()

            # ✅ Échelle X forcée
            if len(all_x) > 1:
                min_x = min(all_x)
                max_x = max(all_x)
                ax.set_xlim(min_x - 1, max_x + 1)
                print("✅ Limites X définies :", min_x - 1, "→", max_x + 1)

            if len(all_x) > 0 and len(all_y) > 0:
                mpl_add_tooltips(self.figure, ax, np.array(all_x), np.array(all_y), labels=all_labels)
                mpl_add_crosshair(self.figure, ax)
                mpl_add_brush_zoom(self.figure, ax)
                self._original_xlim = ax.get_xlim()
                self._original_ylim = ax.get_ylim()
                mpl_add_doubleclick_reset(self.figure, ax, self._original_xlim, self._original_ylim)
                mpl_add_context_menu(self.figure, ax, [
                    ("Enregistrer l'image", self.save_graphic),
                    ("Réinitialiser le zoom", self.reset_zoom)
                ])
                mpl_add_export_button(self.figure, self.canvas)

            self.canvas.draw()

        except Exception as e:
            show_error(self, "Erreur graphique", f"Impossible d'afficher le graphique :\n{e}")

    def save_graphic(self):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le graphique", "", "PNG (*.png);;PDF (*.pdf)")
        if path:
            try:
                self.figure.savefig(path)
                show_info(self, "Succès", f"Graphique enregistré avec succès :\n{path}")
            except Exception as e:
                show_error(self, "Erreur", f"Échec de l'enregistrement :\n{e}")

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exporter CSV", "", "CSV (*.csv)")
        if path:
            try:
                if isinstance(self.data, pd.DataFrame):
                    self.data.to_csv(path, index=False)
                elif isinstance(self.data, dict):
                    df_combined = pd.concat(self.data.values(), keys=self.data.keys(), names=["Scénario", "Index"])
                    df_combined.to_csv(path)
                show_info(self, "Succès", f"Export CSV réussi :\n{path}")
            except Exception as e:
                show_error(self, "Erreur", f"Erreur lors de l'export CSV :\n{e}")

    def reset_zoom(self):
        if self._original_xlim and self._original_ylim:
            ax = self.figure.axes[0]
            ax.set_xlim(self._original_xlim)
            ax.set_ylim(self._original_ylim)
            self.canvas.draw()
