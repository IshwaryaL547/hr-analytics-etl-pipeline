"""
logger.py

Centralized application logger.
"""

import logging

from pathlib import Path

from config.config import Config


Config.LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = (
    Config.LOG_DIR /
    "pipeline.log"
)

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            LOG_FILE
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(
    "HRAnalyticsPipeline"
)