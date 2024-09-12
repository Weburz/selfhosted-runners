#!/usr/bin/env python3

"""Script to uninstall and remove the self-hosted GitHub Action runners.

The script is made publicly available under the terms and conditions of the MIT
license. You will find more information about the distribution and usage copyright
guidelines in the LICENSE file linked below:
https://github.com/Weburz/selfhosted-runners/blob/main/LICENSE

Follow the instructions below for a brief usage guideline of the script:

    1. Ensure the script is executable by invoking "chmod u+x remove.py".
    2. Get the help texts by invoking "./remove.py --help".
"""

import argparse
import logging
import pathlib


def main() -> None:
    """Entrypoint to the script.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    logging.basicConfig(format="[INFO] %(message)s", level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="remove one or all existing selfhosted GitHub Action runners"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="remove all existing runners from the host",
    )

    parser.add_argument(
        "--runner",
        type=str,
        help="remove a particular existing runner from the host, if it exists",
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        help='remove the runners from the specified location, defaults to "."',
        default=pathlib.Path.cwd(),
    )

    args = parser.parse_args()

    if args.all:
        logging.info("Removing all existing runners")

    if args.runner:
        logging.info("Remove the runner - %s", args.runner)


def remove_all_runners() -> None:
    """Remove all existing runners on the host."""


def remove_individual_runner() -> None:
    """Remove an individual runner which is identified by its unique ID."""


if __name__ == "__main__":
    main()
