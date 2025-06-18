from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.results_window import (
    TabSummary,
    TabByYear,
    TabByYearFiltered,
    TabCSVExport,
    TabCSVInteractive       # ✅ Renommé ici (anciennement TabCSVImport)
)
from ui.results_window.logger import logger
from ui.widgets.fade_tab_widget import FadeTabWidget  # ✅ Transition animée

class ResultsWindow(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Résultats de Simulation")
        self.setGeometry(270, 270, 1000, 680)

        self.init_ui()

        if logger:
            logger.info("ResultsWindow ouverte avec données : %s", "OK" if self.data is not None else "None")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.tabs = FadeTabWidget()
        layout.addWidget(self.tabs)

        self.tab_summary = TabSummary(self.data)
        self.tabs.addTab(self.tab_summary, "📊 Résumé")

        self.tab_by_year = TabByYear(self.data)
        self.tabs.addTab(self.tab_by_year, "📆 Annuel (moyennes)")

        self.tab_by_year_filtered = TabByYearFiltered(self.data)
        self.tabs.addTab(self.tab_by_year_filtered, "🔍 Filtres dynamiques")

        self.tab_csv_export = TabCSVExport(self.data)
        self.tabs.addTab(self.tab_csv_export, "📁 Export CSV")

        self.tab_csv_interactive = TabCSVInteractive(self.data)  # ✅ nom mis à jour
        self.tabs.addTab(self.tab_csv_interactive, "🧾 CSV interactif")

        self.tabs.setCurrentIndex(0)
        self.tabs.show()
        self.tabs.repaint()
        self.tabs.update()
        self.update()
        self.show()
