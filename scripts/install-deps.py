#!/usr/bin/env python3

"""Script to install the tools and dependencies on the server hosting the runners."""

import logging
import os
import subprocess
import sys

# The ANSI colour codes for the log messages
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

formatter = logging.Formatter("%(color)s[%(levelname)s]%(reset)s %(message)s")


def add_color_to_record(record: logging.LogRecord) -> logging.LogRecord:
    """A utility function to add some colours to the log messages.

    Args:
        record: A LogRecord instance

    Returns:
        A customised LogRecord instance

    Raises:
        None
    """
    match record.levelno:
        case logging.ERROR:
            record.color = RED
        case record.levelno:
            record.color = BLUE
        case _:
            record.color = ""

    record.reset = RESET

    return record


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addFilter(add_color_to_record)


def install_unzip() -> None:
    """Install the "unzip" tool on the server."""
    logger.info('Installing "unzip"')
    subprocess.run(["sudo", "apt-get", "install", "unzip"])  # noqa: S607, S603


def main() -> None:
    """The entrypoint of the script.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    install_unzip()


if __name__ == "__main__":
    # Check if script invoked by the "root" user, if so throw error message and exit
    if not os.geteuid() == 0:
        main()
    else:
        logger.error("Must run script as non-root user!")
        sys.exit(1)
