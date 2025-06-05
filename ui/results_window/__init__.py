# ui/results_window/__init__.py

from .results_window import ResultsWindow
from .tab_summary import TabSummary
from .tab_by_year import TabByYear
from .tab_csv_export import TabCSVExport
from .tab_csv_import import TabCSVImport

# Optionally, expose a logger (if you use one in this subpackage)
try:
    from utils.logger import get_child_logger
    logger = get_child_logger("ui.results_window")
except ImportError:
    logger = None

__all__ = [
    "ResultsWindow",
    "TabSummary",
    "TabByYear",
    "TabCSVExport",
    "TabCSVImport",
    "logger"
]
