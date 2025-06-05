import logging
import sys
import os

# --- 1. Central 'app' logger singleton ---
logger = logging.getLogger("app")

# --- 2. Setup Handlers ---
if not logger.hasHandlers():
    # Console Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_level = os.environ.get("APP_LOG_CONSOLE_LEVEL", "INFO").upper()
    stream_handler.setLevel(getattr(logging, stream_level, logging.INFO))
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File Handler (optional)
    log_path = os.environ.get("APP_LOG_FILE", "logs/app.log")
    file_level = os.environ.get("APP_LOG_FILE_LEVEL", "DEBUG").upper()
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    if not any(
        isinstance(h, logging.FileHandler) and
        os.path.abspath(getattr(h, "baseFilename", "")) == os.path.abspath(log_path)
        for h in logger.handlers
    ):
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, file_level, logging.DEBUG))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

# --- 3. Set global log level ---
default_level = os.environ.get("APP_LOG_LEVEL", "DEBUG").upper()
logger.setLevel(getattr(logging, default_level, logging.DEBUG))
for h in logger.handlers:
    h.setLevel(getattr(logging, default_level, logging.DEBUG))

# --- 4. Public API ---
def get_logger(name: str = "app") -> logging.Logger:
    return logger if name == "app" else logger.getChild(name)

def get_child_logger(name: str) -> logging.Logger:
    return get_logger(name)

def set_log_level(level_name: str):
    """Change the global log level at runtime."""
    level = getattr(logging, level_name.upper(), logging.INFO)
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

def add_file_handler(path: str, level: str = "DEBUG"):
    """Add a custom file handler at runtime."""
    log_dir = os.path.dirname(path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    already_added = any(
        isinstance(h, logging.FileHandler) and
        os.path.abspath(getattr(h, "baseFilename", "")) == os.path.abspath(path)
        for h in logger.handlers
    )
    if not already_added:
        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level.upper(), logging.DEBUG))
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

def close_handlers():
    """Close all log handlers (e.g., for rotation or shutdown)."""
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)

# --- 5. Optional import log message ---
logger.debug("✅ Logger initialized from utils/logger.py")

# --- 6. Explicit exports ---
__all__ = [
    "get_logger",
    "get_child_logger",
    "set_log_level",
    "add_file_handler",
    "close_handlers"
]
