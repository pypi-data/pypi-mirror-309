#!/usr/bin/env python

"""utils.py"""

import logging
import subprocess
from re import sub

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run_command(command: str):
    logger.debug("Running command: %s", command)
    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
        )
        logger.debug("Command output:\n%s", process.stdout)
        logger.debug("Command error:\n%s", process.stderr)
    except subprocess.CalledProcessError as error:
        logger.error("Command failed with return code: %s", error.returncode)
        logger.error("Output:\n%s", error.stdout)
        logger.error("Error output:\n%s", error.stderr)
