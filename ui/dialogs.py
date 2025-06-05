# ui/dialogs.py

from PyQt5.QtWidgets import (
    QMessageBox, QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
)
from PyQt5.QtCore import Qt

def show_error(message, parent=None):
    """Affiche une boîte de dialogue d'erreur bloquante."""
    QMessageBox.critical(parent, "Erreur", str(message))

def show_info(message, parent=None):
    """Affiche une boîte de dialogue d'information."""
    QMessageBox.information(parent, "Information", str(message))

def show_warning(message, parent=None):
    """Affiche une boîte de dialogue d'avertissement."""
    QMessageBox.warning(parent, "Avertissement", str(message))

def show_success_export(path, parent=None):
    """Affiche une boîte de succès pour un export effectué."""
    show_info(f"Export effectué avec succès !\n\nFichier : {path}", parent=parent)

def show_export_error(err, parent=None):
    """Affiche une erreur spécifique lors de l'export CSV."""
    show_error(f"Erreur lors de l'export du CSV :\n{err}", parent=parent)

def show_nothing_to_export(parent=None):
    """Affiche un warning si aucune donnée à exporter."""
    show_warning("Aucune donnée à exporter (table vide ou filtre trop restrictif).", parent=parent)

def validate_required_columns(df, required, parent=None):
    """
    Vérifie la présence des colonnes nécessaires dans un DataFrame.
    Affiche une erreur et retourne False si colonnes manquantes.
    """
    missing = [col for col in required if col not in df.columns]
    if missing:
        show_error(f"Colonnes manquantes dans le CSV : {', '.join(missing)}", parent)
        return False
    return True

class DataFramePreviewDialog(QDialog):
    """Boîte de dialogue pour prévisualiser un DataFrame (max 100 lignes, 10 colonnes)."""
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aperçu du fichier CSV")
        self.setMinimumSize(600, 350)
        layout = QVBoxLayout(self)
        n_rows = min(len(df), 100)
        n_cols = min(len(df.columns), 10)
        table = QTableWidget(n_rows, n_cols)
        table.setHorizontalHeaderLabels(list(df.columns)[:n_cols])
        for i in range(n_rows):
            for j in range(n_cols):
                value = str(df.iloc[i, j])
                table.setItem(i, j, QTableWidgetItem(value))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table)
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

def show_preview_dataframe(df, parent=None):
    """Ouvre une fenêtre modale pour prévisualiser le DataFrame."""
    dlg = DataFramePreviewDialog(df, parent)
    dlg.exec_()

# --- BONUS : Helper général pour confirmer un export dans n'importe quel widget ---
def confirm_export_success(path, parent=None):
    QMessageBox.information(parent, "Export réussi", f"Le fichier a été exporté vers :\n{path}")

def confirm_export_failure(path, err, parent=None):
    QMessageBox.critical(parent, "Export échoué", f"Erreur lors de l'export dans {path}\n\nDétail :\n{err}")

# ------------- Exemples d'utilisation --------------
# from ui.dialogs import show_error, show_preview_dataframe, show_success_export, show_nothing_to_export
#
# show_success_export("data/output/export.csv", parent=self)
# show_nothing_to_export(parent=self)
