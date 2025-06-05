# core/__init__.py

from .employee import Employee
from .germes import GermesAlea
from .retiree import Retiree
from .scenario import Scenario
from .simulator import Simulator

# Optional: Get a logger for this package (sub-logger of "app")
try:
    from utils.logger import get_child_logger
    logger = get_child_logger("core")
except ImportError:
    import logging
    logger = logging.getLogger("app.core")

# This logger is available as core.logger and will write to your global log
logger.debug("core package imported and logger initialized.")

# __all__ so `from core import *` works in tests or debugging
__all__ = [
    "Employee",
    "GermesAlea",
    "Retiree",
    "Scenario",
    "Simulator",
    "logger",
]
