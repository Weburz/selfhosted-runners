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
import json
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.request


def main() -> None:
    """Entrypoint to the script.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="remove one or all existing selfhosted GitHub Action runners"
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
        help='remove the runners from the specified location, defaults to "./runners"',
        default=pathlib.Path(pathlib.Path.cwd() / "runners"),
    )

    parser.add_argument(
        "--pat",
        type=str,
        help="the personal access token to authorize removal of the runner from GitHub",
        required=True,
    )

    args = parser.parse_args()

    # Remove all runners if not particular runner is specified
    if not args.runner:
        if confirm_action(
            "Removing all GitHub Action runners from the host! Confirm? [y/N] "
        ):
            remove_all_runners(runner_path=args.location, pat=args.pat)
            sys.exit(0)
        else:
            sys.exit(1)

    # Remove a single specified runner
    if args.runner:
        answer = input(
            f"Removing the GitHub Action runner - {args.runner}! Confirm? [y/N]"
        )

        if answer.lower() in ("y", "yes"):
            logging.info("Removed the runner %s from %s", args.runner, args.location)
            remove_individual_runner(
                runner_path=pathlib.Path(pathlib.Path.cwd() / "runners"),
                id=args.runner,
                pat=args.pat,
            )
            sys.exit(0)
        elif answer.lower() in ("n", "no"):
            sys.exit(1)


def confirm_action(prompt: str) -> bool:
    """Prompt the user whether to perform a certain action or not.

    Args:
        prompt: The string to prompt the user with.

    Returns:
        boolean

    Raises:
        None
    """
    while True:
        answer = input(prompt).lower()

        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):  # noqa: RET505
            return False
        else:
            print("Please answer 'yes' or 'no'.")


def remove_all_runners(runner_path: pathlib.Path, pat: str) -> None:
    """Remove all existing runners on the host.

    Args:
        runner_path: The file path, where the runners are installed at. Default: "."
        pat: The Personal Access Token (PAT) to remove the runners from GitHub.

    Returns:
        None

    Raises:
        None
    """
    original_dir = pathlib.Path.cwd()
    token = get_token(pat)

    if not runner_path.exists() and not runner_path.is_dir():
        logging.error("[ERROR] No runners found in the directory %s", runner_path)
        sys.exit(1)
    else:
        for runner in runner_path.iterdir():
            os.chdir(runner)
            subprocess.run(["sudo", "./svc.sh", "stop"])  # noqa: S603, S607
            subprocess.run(["sudo", "./svc.sh", "uninstall"])  # noqa: S603, S607
            subprocess.run(["./config.sh", "remove", "--token", token])  # noqa: S603
            logging.info(
                "[INFO] Runner %s removed and unconfigured from GitHub", runner
            )
            os.chdir(original_dir)

        shutil.rmtree(runner_path)
        logging.info("[INFO] All runners cleaned up from the host")


def remove_individual_runner(runner_path: pathlib.Path, id: str, pat: str) -> None:
    """Remove an individual runner which is identified by its unique ID.

    Args:
        runner_path: The location to search for existing runners, defaults to "."
        id: The unique ID of the runner to remove.
        pat: The Personal Access Token (PAT) to remove the runner from GitHub.

    Returns:
        None

    Raises:
        None
    """
    original_dir = pathlib.Path.cwd()
    runner_dir = pathlib.Path(pathlib.Path.cwd() / runner_path / id)
    token = get_token(pat)

    if runner_dir.exists() and runner_dir.is_dir():
        os.chdir(runner_dir)

        # Stop the runner's background service
        subprocess.run(["sudo", "./svc.sh", "stop"])  # noqa: S603 S607
        subprocess.run(["sudo", "./svc.sh", "uninstall"])  # noqa: S603 S607

        # Remove the runner from GitHub
        subprocess.run(["./config.sh", "remove" "--token", token])  # noqa: S603

        os.chdir(original_dir)

        # Delete the entire directory where the runner was configured and stored
        shutil.rmtree(runner_dir)
    else:
        logging.error(
            "[ERROR] The runner - %s was not found at location: %s",
            id,
            pathlib.Path(runner_path / id),
        )
        sys.exit(1)


def get_token(pat: str) -> str:
    """Get a token to register the runners on GitHub with.

    Args:
        pat: This is the Personal Access Token (PAT) used to generate the token.

    Returns:
        None

    Raises:
        None
    """
    url = "https://api.github.com/orgs/Weburz/actions/runners/registration-token"
    req = urllib.request.Request(  # noqa: S310
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {pat}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as response:  # noqa: S310
        data = response.read()
        result = json.loads(data.decode("utf-8"))

    return result.get("token")


if __name__ == "__main__":
    # Check if script invoked by the "root" user, if so throw error message and exit
    if not os.geteuid() == 0:
        main()
    else:
        logging.error("[ERROR] Must run script as non-root user!")
        sys.exit(1)
