from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.results_window import TabSummary, TabByYear, TabCSVExport
from ui.results_window import logger

# NEW: Import FadeTabWidget for fade-in tab transitions
from ui.widgets.fade_tab_widget import FadeTabWidget

class ResultsWindow(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Résultats de Simulation")
        self.setGeometry(270, 270, 900, 650)
        self.data = data  # À partager avec les tabs si besoin
        self.init_ui()
        logger.info("ResultsWindow ouverte avec données %s", "OK" if data is not None else "None")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # USE FadeTabWidget instead of QTabWidget!
        self.tabs = FadeTabWidget()
        layout.addWidget(self.tabs)

        self.tab_summary = TabSummary(self.data)
        self.tabs.addTab(self.tab_summary, "Résumé")

        self.tab_by_year = TabByYear(self.data)
        self.tabs.addTab(self.tab_by_year, "Résultats annuels")

        self.tab_csv_export = TabCSVExport(self.data)
        self.tabs.addTab(self.tab_csv_export, "Export CSV")
