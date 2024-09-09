#!/usr/bin/env python3

"""Script to install and setup the self-hosted GitHub Action runners.

The script is made publicly available under the terms and conditions of the MIT
license. You will find more information about the distribution and usage copyright
guidelines in the LICENSE file linked below:
https://github.com/Weburz/selfhosted-runners/blob/main/LICENSE

For more information
on the tool, refer to the documentations accessible at:
https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners

Follow the instructions below for a brief usage guideline of the script:

    1. Ensure the script is executable by invoking "chmod u+x install.py".
    2. Get the help texts by invoking "./install.py --help".
    3. Install N number of runners by invoking "./install.py -n N", where N is the
       number of runners to deploy on the host.
"""

import argparse
import pathlib
import uuid


def main() -> None:
    """Entrypoint of the script.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    # Initialise the ArgumentParser object
    parser = argparse.ArgumentParser(
        description="install and setup the self-hosted GitHub Action runners."
    )

    # Add the arguments for the script
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=1,
        help="the number of runners to spin up (default: 1)",
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        help="the location on the host to install the runners at (default: pwd)",
    )

    # Generate the list of arguments for further processing
    args = parser.parse_args()

    # Install and setup the runners on the remote host
    setup_runner(args.number, location=args.location)


def setup_runner(n: int = 1, location: str | None = None) -> None:
    """Install and setup the GitHub Action selfhosted runners.

    Args:
        n: Install n number of runners on the host.
        location: The location to install the runners at.

    Returns:
        None

    Raises:
        None
    """
    # Create a list of uniquely named directories to store the runners under.
    dir_uuids = [str(uuid.uuid4()).split("-")[0] for _ in range(int(n))]

    if not location:
        runner_dir = pathlib.Path(pathlib.Path.cwd() / "runners")
    else:
        runner_dir = pathlib.Path(
            pathlib.Path.home() / pathlib.Path(location) / "runners"
        )

    print(f"Creating {n} directories to install the runners under:")
    for idx in range(len(dir_uuids)):
        print(f"{idx + 1}: {runner_dir}/{dir_uuids[idx]}")
        pathlib.Path(runner_dir / dir_uuids[idx]).mkdir(exist_ok=True, parents=True)


if __name__ == "__main__":
    main()
