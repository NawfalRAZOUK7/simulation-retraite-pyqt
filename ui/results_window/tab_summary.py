from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
import pandas as pd
from ui.results_window import logger  # Ajout du logger

class TabSummary(QWidget):
    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout(self)

        label = QLabel("<b>Résumé des Résultats</b>")
        layout.addWidget(label)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.show_summary(data)

    def show_summary(self, data):
        if data is None or not isinstance(data, pd.DataFrame):
            self.text.setText("Aucune donnée à afficher.")
            logger.warning("Aucune donnée reçue dans TabSummary.")
            return
        # Exemple d'analyse : moyenne et intervalle de confiance de la réserve finale
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
            logger.error("Erreur dans show_summary : %s", str(e))
        self.text.setText(msg)
