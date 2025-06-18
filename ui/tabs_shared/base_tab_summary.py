# ui/tabs_shared/base_tab_summary.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
import pandas as pd
from ui.results_window.logger import logger

class BaseTabSummary(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data
        self.layout = QVBoxLayout(self)
        self.init_ui()

    def init_ui(self):
        label = QLabel("<b>Résumé des Résultats</b>")
        self.layout.addWidget(label)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)

        self.show_summary(self.data)

    def show_summary(self, data):
        if data is None or not isinstance(data, pd.DataFrame):
            self.text.setText("Aucune donnée à afficher.")
            logger.warning("Aucune donnée reçue dans BaseTabSummary.")
            return

        try:
            reserves = data[data["Annee"] == 2035]["Reserve"]
            moyenne = reserves.mean()
            std = reserves.std(ddof=1)
            n = reserves.shape[0]
            ic_low = moyenne - 1.96 * std / (n ** 0.5)
            ic_high = moyenne + 1.96 * std / (n ** 0.5)
            msg = (
                f"Réserve moyenne finale (2035) : {moyenne:,.0f} DH\n"
                f"Intervalle de confiance à 95% : [{ic_low:,.0f}, {ic_high:,.0f}] DH\n"
                f"Nombre de simulations : {n}"
            )
            logger.info("Résumé affiché : moyenne=%.0f, IC=[%.0f, %.0f], n=%d", moyenne, ic_low, ic_high, n)
        except Exception as e:
            msg = f"Erreur lors du calcul : {e}"
            logger.error("Erreur dans BaseTabSummary : %s", str(e))

        self.text.setText(msg)
