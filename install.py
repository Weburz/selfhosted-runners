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
import logging
import json
import os
import pathlib
import subprocess
import tarfile
import urllib.request
import uuid

logger = logging.getLogger(__name__)


def main() -> None:
    """Entrypoint of the script.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    logging.basicConfig(format="[INFO] %(message)s", level=logging.INFO)

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

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="The URL of the organisation on GitHub to setup the runners for",
    )

    parser.add_argument(
        "--pat",
        type=str,
        required=True,
        help="The Personal Access Token used to authenticate to the GitHub servers.",
    )

    # Generate the list of arguments for further processing
    args = parser.parse_args()

    # Install and setup the runners on the remote host
    setup_runner(url=args.url, n=args.number, location=args.location, pat=args.pat)


def setup_runner(pat: str, url: str, n: int = 1, location: str | None = None) -> None:
    """Install and setup the GitHub Action selfhosted runners.

    Args:
        pat: The Personal Access Token (PAT) to authenticate to the GitHub servers.
        url: The URL of the organisation on GitHub to configure the runners at.
        n: Install n number of runners on the host.
        location: The location to install the runners at.

    Returns:
        None

    Raises:
        None
    """
    # Create a list of uniquely named directories to store the runners under.
    dir_uuids = [str(uuid.uuid4()).split("-")[0] for _ in range(int(n))]
    # TODO (Somraj Saha): Figure a way out to fetch a specific version (or the latest
    # version of the runner)
    # 001
    runner_version = get_latest_runner()

    # Create the directories in the specified location
    if not location:
        create_directories(n=n, dir_uuids=dir_uuids)
    else:
        create_directories(n=n, dir_uuids=dir_uuids, location=location)

    # Download the runners to each of their directory
    for directory in dir_uuids:
        logger.info("Downloading GitHub Action runner v%s", runner_version)
        logger.info(
            "Extracting the tarfile before setting up the runner - %s", directory
        )
        download_runners(
            version=runner_version,
            path=pathlib.Path(pathlib.Path.cwd() / "runners" / directory),
        )

    for directory in dir_uuids:
        logger.info("Configuring the %s runner", directory)
        configure_runner(url=url, name=directory, runner_id=directory, pat=pat)

    for directory in dir_uuids:
        logger.info("Starting the runner %s as a background service", directory)
        create_runner_service(runner_id=directory)


def get_latest_runner() -> str:
    """Fetch the latest release version of the selfhosted runners.

    Args:
        None

    Returns:
        The latest version number of the runner (example - v2.319.1)

    Raises:
        None
    """
    url = "https://api.github.com/repos/actions/runner/releases/latest"

    with urllib.request.urlopen(url) as response:  # noqa: S310
        data = json.loads(response.read().decode())
        return data.get("tag_name")


def create_directories(
    n: int, dir_uuids: list[str], location: str | None = None
) -> None:
    """Create the directories to install and setup the runners under.

    Args:
        n: Create n number of directories to install the runners at.
        dir_uuids: A list of shortened UUID strings to identify a runner with.
        location: The location to install the runner at. Defaults to the current
        directory.

    Returns:
        None

    Raises:
        None
    """
    dir_uuids = dir_uuids

    if not location:
        runner_dir = pathlib.Path(pathlib.Path.cwd() / "runners")
    else:
        runner_dir = pathlib.Path(
            pathlib.Path.home() / pathlib.Path(location) / "runners"
        )

    logger.info("Creating %s directories to install the runners under:", n)
    for idx in range(len(dir_uuids)):
        logger.info("%s/%s", runner_dir, dir_uuids[idx])
        pathlib.Path(runner_dir / str(dir_uuids[idx])).mkdir(
            exist_ok=True, parents=True
        )


def download_runners(version: str, path: pathlib.Path, arch: str = "x64") -> None:
    """Download the runners from GitHub.

    Args:
        version: The runner version to download from GitHub.
        path: The path on the filesystem to download the runners to.
        arch: The system architecture of the runners to download. Defaults to "x64".

    Returns:
        None

    Raises:
        None
    """
    base_url = "https://github.com/actions/runner/releases/download/"
    tarball = f"{base_url}v{version}/actions-runner-linux-{arch}-{version}.tar.gz"

    stream = urllib.request.urlopen(tarball)  # noqa: S310
    file = tarfile.open(fileobj=stream, mode="r:gz")

    file.extractall(path=path, filter="fully_trusted")  # noqa 202


def configure_runner(url: str, pat: str, name: str, runner_id: str) -> None:
    """Install and setup the runners as background services.

    Args:
        url: The URL of the organisation (or repository) to configure the runners on.
        pat: The Personal Access Token to use for configuring the runner.
        name: The name of the runner to assign and show on the GitHub Web UI.
        runner_id: The ID of the runner to configure.

    Returns:
        None

    Raises:
        None
    """
    root_dir = pathlib.Path.cwd()
    runner_dir = pathlib.Path(root_dir / "runners" / runner_id)
    cmd = [
        f"{runner_dir}/config.sh",
        "--unattended",
        "--url",
        url,
        "--pat",
        pat,
        "--name",
        name,
    ]

    os.chdir(runner_dir)
    subprocess.run(cmd)  # noqa: S603
    os.chdir(root_dir)


def create_runner_service(runner_id: str) -> None:
    """Create a background service.

    Args:
        runner_id: The ID of the runner to run as a background service.

    Returns:
        None

    Raises:
        None
    """
    root_dir = pathlib.Path.cwd()
    runner_dir = pathlib.Path(root_dir / "runners" / runner_id)

    os.chdir(runner_dir)
    subprocess.run(["sudo", f"{runner_dir}/svc.sh", "install"])  # noqa: S603, S607
    subprocess.run(["sudo", f"{runner_dir}/svc.sh", "start"])  # noqa: S603, S607
    os.chdir(root_dir)


if __name__ == "__main__":
    main()
