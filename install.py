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


def main() -> None:
    """Entrypoint of the script."""
    print("Hello World!")


if __name__ == "__main__":
    main()
