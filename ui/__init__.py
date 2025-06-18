# ui/__init__.py

from utils.logger import get_child_logger

# UI logger for all UI submodules (consistent style everywhere)
logger = get_child_logger("ui")

# --- Main Windows ---
from .menu_window import MenuWindow
from .settings_window import SettingsWindow
from .simulation_window import SimulationWindow

# --- Dialogs and Helpers ---
from .dialogs import (
    show_error,
    show_info,
    show_warning,
    show_success_export,
    show_export_error,
    show_nothing_to_export,
    show_preview_dataframe,
    validate_required_columns,
    confirm_export_success,
    confirm_export_failure,
    DataFramePreviewDialog,
)

from .progress_dialog import ProgressDialog

# --- Themeing ---
from .theme import get_custom_palette, get_dark_palette

from .graph_window import GraphWindow

from .report_window import ReportWindow

# --- Widgets (expose as needed, you can add more) ---
# Example: from .widgets.animated_tool_button import AnimatedToolButton

__all__ = [
    "MenuWindow",
    "SettingsWindow",
    "SimulationWindow",
    "ProgressDialog",
    "show_error",
    "show_info",
    "show_warning",
    "show_success_export",
    "show_export_error",
    "show_nothing_to_export",
    "show_preview_dataframe",
    "validate_required_columns",
    "confirm_export_success",
    "confirm_export_failure",
    "DataFramePreviewDialog",
    "get_custom_palette",
    "get_dark_palette",
    "logger",
    "GraphWindow"
    # Add widget classes here if you want to expose them globally
]
