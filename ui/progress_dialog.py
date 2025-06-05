# ui/progress_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class ProgressDialog(QDialog):
    def __init__(self, message="Veuillez patienter...", max_steps=4):
        super().__init__()
        self.setWindowTitle("Traitement en cours")
        self.setModal(True)
        layout = QVBoxLayout(self)
        label = QLabel(message)
        label.setStyleSheet("font-size:16px; padding:10px;")
        layout.addWidget(label)
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(max_steps)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        self.setFixedSize(340, 120)

    def set_step(self, step):
        self.progress.setValue(step)
