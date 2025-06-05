# core/__init__.py

from .employee import Employee
from .germes import GermesAlea
from .retiree import Retiree
from .scenario import Scenario
from .simulator import Simulator

# __all__ so `from core import *` works in tests or debugging
__all__ = [
    "Employee",
    "GermesAlea",
    "Retiree",
    "Scenario",
    "Simulator",
]
