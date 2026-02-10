# src/logger.py
import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    """
    Central project logger.
    Writes to logs/provisioning.log as required by the project spec.
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "provisioning.log"

    logger = logging.getLogger("infra-automation")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if imported multiple times
    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# IMPORTANT: this is what infra_simulator imports
logger = setup_logger()
