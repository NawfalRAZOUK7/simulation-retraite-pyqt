# utils/logger.py

import logging
import sys
import os

# --- 1. Central 'app' logger singleton ---
logger = logging.getLogger("app")

# --- 2. Handler(s) ---

if not logger.hasHandlers():
    # Console Handler (default)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_level = os.environ.get("APP_LOG_CONSOLE_LEVEL", "INFO").upper()
    stream_handler.setLevel(getattr(logging, stream_level, logging.INFO))
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # --- 2b. Option: File handler (auto-create log dir, deduplicate, env level) ---
    log_path = os.environ.get("APP_LOG_FILE", "logs/app.log")
    file_level = os.environ.get("APP_LOG_FILE_LEVEL", "DEBUG").upper()
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Only add file handler if not already present for this path
    file_handler_exists = any(
        isinstance(h, logging.FileHandler) and
        getattr(h, "baseFilename", None) and
        os.path.abspath(h.baseFilename) == os.path.abspath(log_path)
        for h in logger.handlers
    )
    if not file_handler_exists:
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, file_level, logging.DEBUG))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

# --- 3. Default Level (overridable by env) ---
level = os.environ.get("APP_LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, level, logging.INFO))

# --- 4. Child logger helper ---
def get_child_logger(name: str):
    """Get a child logger, e.g. 'app.ui' or 'app.core.simulator'."""
    return logger.getChild(name)

# --- 5. Utilities ---

def set_log_level(level_name: str):
    """Set the log level globally (e.g., 'DEBUG', 'INFO', 'WARNING')."""
    logger.setLevel(getattr(logging, level_name.upper(), logging.INFO))
    for handler in logger.handlers:
        handler.setLevel(getattr(logging, level_name.upper(), logging.INFO))

def add_file_handler(path: str, level: str = "DEBUG"):
    """Add a file handler at runtime."""
    log_dir = os.path.dirname(path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    # Avoid duplicate file handler
    file_handler_exists = any(
        isinstance(h, logging.FileHandler) and
        getattr(h, "baseFilename", None) and
        os.path.abspath(h.baseFilename) == os.path.abspath(path)
        for h in logger.handlers
    )
    if not file_handler_exists:
        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level.upper(), logging.DEBUG))
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

def close_handlers():
    """Close all handlers and flush output (for log rotation or shutdown)."""
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)

# --- 6. Example: log on import (optional, comment if you dislike) ---
logger.debug("Logger initialized in utils/logger.py")

# --- 7. __all__ (optional, for explicit import) ---
__all__ = ["logger", "get_child_logger", "set_log_level", "add_file_handler", "close_handlers"]

