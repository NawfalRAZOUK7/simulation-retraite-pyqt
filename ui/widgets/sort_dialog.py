# ui/results_window/sort_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QCheckBox, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

class SortDialog(QDialog):
    """
    Boîte de dialogue pour choisir un tri multi-colonnes, ordre croissant/décroissant.
    """
    def __init__(self, columns, parent=None, prev_columns=None, prev_orders=None):
        super().__init__(parent)
        self.setWindowTitle("Tri multi-colonnes")
        self.setMinimumWidth(350)
        self.columns = columns

        # Persistance des choix précédents (optionnel)
        prev_columns = prev_columns or []
        prev_orders = prev_orders or []

        self.selected_columns = []
        self.orders = []

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(QLabel("Choisissez les colonnes à trier (dans l’ordre) :"))

        # Section multi-colonnes (ComboBox + CheckBox)
        self.combo_boxes = []
        self.check_boxes = []
        max_cols = min(4, len(columns))  # Permettre jusqu'à 4 tris imbriqués (modifie selon besoin)
        for i in range(max_cols):
            row = QHBoxLayout()
            combo = QComboBox()
            combo.addItems([''] + columns)
            if i < len(prev_columns):
                idx = combo.findText(prev_columns[i])
                if idx >= 0:
                    combo.setCurrentIndex(idx)
            row.addWidget(combo)
            self.combo_boxes.append(combo)

            chk = QCheckBox("Décroissant")
            if i < len(prev_orders) and prev_orders[i] is False:
                chk.setChecked(False)
            elif i < len(prev_orders) and prev_orders[i] is True:
                chk.setChecked(True)
            row.addWidget(chk)
            self.check_boxes.append(chk)

            self.vbox.addLayout(row)

        # Boutons
        btn_row = QHBoxLayout()
        self.btn_ok = QPushButton("Valider")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(self.btn_ok)
        btn_row.addWidget(self.btn_cancel)
        self.vbox.addLayout(btn_row)

    def get_result(self):
        """Retourne deux listes : colonnes à trier et ordres True(croissant)/False(décroissant)."""
        columns = []
        orders = []
        for combo, chk in zip(self.combo_boxes, self.check_boxes):
            col = combo.currentText().strip()
            if col and col not in columns:
                columns.append(col)
                orders.append(not chk.isChecked())  # True si croissant, False si décroissant
        return columns, orders
