from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QCheckBox, QLabel, QPushButton, QHBoxLayout, QFileDialog
)
import os

class ReportExportDialog(QDialog):
    """
    Dialogue pour choisir les sections à inclure dans le PDF (Résumé, Statistiques, Graphiques).
    Retourne (path, [sections]) ou (None, None) si annulé.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exporter le rapport PDF")
        self.setMinimumWidth(430)
        self.selected_sections = []
        self.export_path = None

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Sections à inclure dans le rapport PDF :</b>"))
        self.cb_summary = QCheckBox("Inclure le résumé (texte d’introduction)")
        self.cb_stats = QCheckBox("Inclure les statistiques (tableaux/résumés)")
        self.cb_figures = QCheckBox("Inclure les graphiques (plots, courbes)")
        self.cb_summary.setChecked(True)
        self.cb_stats.setChecked(True)
        self.cb_figures.setChecked(True)
        layout.addWidget(self.cb_summary)
        layout.addWidget(self.cb_stats)
        layout.addWidget(self.cb_figures)
        layout.addSpacing(14)

        file_layout = QHBoxLayout()
        self.path_label = QLabel("Aucun fichier choisi.")
        self.choose_btn = QPushButton("Choisir le fichier PDF...")
        self.choose_btn.clicked.connect(self.choose_path)
        file_layout.addWidget(self.choose_btn)
        file_layout.addWidget(self.path_label, 1)
        layout.addLayout(file_layout)
        layout.addSpacing(8)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Exporter")
        self.cancel_btn = QPushButton("Annuler")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def choose_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Choisir l’emplacement du rapport PDF",
            "rapport_simulation.pdf",
            "PDF (*.pdf)"
        )
        if path:
            if not path.lower().endswith(".pdf"):
                path += ".pdf"
            self.export_path = path
            self.path_label.setText(f"<span style='color:#417505;'>{os.path.basename(path)}</span>")

    def get_result(self):
        if not self.export_path:
            return None, None
        sections = []
        if self.cb_summary.isChecked():
            sections.append("summary")
        if self.cb_stats.isChecked():
            sections.append("stats")
        if self.cb_figures.isChecked():
            sections.append("figures")
        return self.export_path, sections
