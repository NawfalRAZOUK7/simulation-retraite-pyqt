# ui/settings_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout,
    QLineEdit, QMessageBox, QComboBox
)
from utils.fileio import load_config, save_config
import logging
from ui import logger  # Import du logger UI

# -- Import AnimatedToolButton --
from ui.widgets.animated_tool_button import AnimatedToolButton

class SettingsWindow(QDialog):
    def __init__(self, config_path="data/config/parametres.json", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres de configuration")
        self.setFixedSize(420, 340)
        self.config_path = config_path
        self.config = load_config(self.config_path)
        self.init_ui()
        logger.info("SettingsWindow ouverte.")

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Configuration par défaut</b>"))

        form = QFormLayout()
        self.edit_ix = QLineEdit(str(self.config.get("IX", 12345)))
        self.edit_iy = QLineEdit(str(self.config.get("IY", 23456)))
        self.edit_iz = QLineEdit(str(self.config.get("IZ", 34567)))
        self.edit_export_path = QLineEdit(self.config.get("export_path", "data/output/"))

        # -- Animated "Parcourir…" Button with Emoji --
        btn_browse = AnimatedToolButton()
        btn_browse.setText("📁 Parcourir…")
        btn_browse.setToolTip("Sélectionner un dossier d'export")
        btn_browse.clicked.connect(self.browse_export_path)

        form.addRow("Gemme IX", self.edit_ix)
        form.addRow("Gemme IY", self.edit_iy)
        form.addRow("Gemme IZ", self.edit_iz)
        form.addRow("Chemin export CSV", self.edit_export_path)
        form.addRow("", btn_browse)

        # Choix du niveau de log global
        self.combo_log_level = QComboBox()
        self.combo_log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        form.addRow("Niveau de log UI", self.combo_log_level)

        levels = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
        current = logging.getLogger("app.ui").level
        for name, val in levels.items():
            if val == current:
                self.combo_log_level.setCurrentText(name)
                break

        layout.addLayout(form)

        # -- Animated "Enregistrer" Button with Emoji --
        btn_save = AnimatedToolButton()
        btn_save.setText("💾 Enregistrer")
        btn_save.setToolTip("Sauvegarder les paramètres")
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)

    def browse_export_path(self):
        from PyQt5.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(self, "Choisir un dossier d'export")
        if path:
            self.edit_export_path.setText(path)
            logger.info("Chemin export CSV modifié : %s", path)

    def save_settings(self):
        try:
            config = {
                "IX": int(self.edit_ix.text()),
                "IY": int(self.edit_iy.text()),
                "IZ": int(self.edit_iz.text()),
                "export_path": self.edit_export_path.text()
            }
            levels = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
            level_name = self.combo_log_level.currentText()
            for logger_name in ["app.ui", "app.ui.results", "app.ui.charts"]:
                logging.getLogger(logger_name).setLevel(levels[level_name])
            logger.info("Niveau de log UI modifié : %s", level_name)

            if save_config(config, self.config_path):
                QMessageBox.information(self, "Succès", "Paramètres sauvegardés avec succès.")
                self.config = config
                logger.info("Paramètres sauvegardés avec succès : %s", config)
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la sauvegarde du fichier.")
                logger.error("Erreur lors de la sauvegarde du fichier de config.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur : {e}")
            logger.error("Erreur dans save_settings : %s", str(e))

# --- Pour test seul ---
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication
#     import sys
#     app = QApplication(sys.argv)
#     win = SettingsWindow()
#     win.exec_()
