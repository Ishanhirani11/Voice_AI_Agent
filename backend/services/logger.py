# backend/services/logger.py

import os
import logging

from backend.config import (
    LOG_FILE,
    LOG_LEVEL
)


# ---------------------------------------------------
# Create log directory
# ---------------------------------------------------

log_directory = os.path.dirname(
    LOG_FILE
)

os.makedirs(
    log_directory,
    exist_ok=True
)


# ---------------------------------------------------
# Configure logger
# ---------------------------------------------------

logging.basicConfig(

    filename=LOG_FILE,

    level=getattr(
        logging,
        LOG_LEVEL.upper()
    ),

    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)


logger = logging.getLogger(
    "voice_agent"
)