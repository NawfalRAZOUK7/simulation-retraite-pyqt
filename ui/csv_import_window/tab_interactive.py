# ui/csv_import_window/tab_interactive.py

from ui.tabs_shared.base_tab_interactive import BaseTabInteractive

class TabCSVInteractive(BaseTabInteractive):
    def __init__(self, data=None):
        super().__init__(data, title="Données CSV interactives")
