# ui/charts_window/__init__.py

from .charts_window import ChartsWindow
from .tab_reserve import TabReserve
from .tab_confidence import TabConfidence
from .tab_comparaison import TabComparaison
from .scenario_selector import ScenarioSelector

# Optionally: expose logger if you use a subpackage-specific logger (not always needed)
try:
    from utils.logger import get_child_logger
    logger = get_child_logger("ui.charts_window")
except ImportError:
    import logging
    logger = logging.getLogger("ui.charts_window")

__all__ = [
    "ChartsWindow",
    "TabReserve",
    "TabConfidence",
    "TabComparaison",
    "ScenarioSelector",
    "logger"
]
