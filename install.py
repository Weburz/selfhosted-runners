#!/usr/bin/env python3

"""Script to install and setup the self-hosted GitHub Action runners.

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


def main() -> None:
    """Entrypoint of the script."""
    # Initialise the ArgumentParser object
    parser = argparse.ArgumentParser(
        description="install and setup the self-hosted GitHub Action runners."
    )

    # Add the arguments for the script
    parser.add_argument(
        "-n",
        "--number",
        default=1,
        help="the number of runners to spin up (default: 1)",
    )

    # Generate the list of arguments for further processing
    args = parser.parse_args()

    # TODO(Somraj Saha): Handle installation and setup of the runners according to the
    # number of runners specified.
    # WEBUR-18
    for n in range(int(args.number)):
        print(f"{n + 1}: 'Hello World!'")


if __name__ == "__main__":
    main()
