#!/usr/bin/env python

"""pyenvcfg to init envcfg setup"""

import locale
import logging
import os
import subprocess

import click
import git
from jcgutier_logger.logger import Logger

from pyenvcfg.utils import utils
from pyenvcfg.version import __version__

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# click cli to call module
@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logs")
@click.version_option(
    __version__, "--version", "-v", message="%(prog)s version %(version)s"
)
def cli(debug=False):
    """Cli command group

    Args:
        debug (bool, optional): To show debug logs. Defaults to False.
    """
    Logger(debug)


@cli.command()
def install():
    """Install pyenvcfg"""
    logger.debug("Installing pyenvcfg...")

    # Pre-required packages
    packages = ["git"]

    # Getting shared config
    local_server = os.getenv("LOCAL_SERVER", "carlos-hp.ts.local")

    # Exporting token to clone repos
    commands = [
        "sudo apt update",
        f"sudo apt install -y {' '.join(packages)}",
        f"scp -pr {local_server}:~/.shared_config/ ~/.shared_config/",
        "export GITLAB_TOKEN=\"$(grep token: ~/.shared_config/glab-cli/config.yml | sed -r 's/ +//g' | cut -d ':' -f2)\"",
        "export GITHUB_TOKEN=\"$(grep oauth_token ~/.shared_config/gh/hosts.yml | sed -r 's/ +//g' | cut -d ':' -f2 | tail -1)\"",
    ]
    for command in commands:
        utils.run_command(command=command)

    # Define envcfg repo
    envcfg_repo = "github.com:jcgutier/envcfg"

    # Create directory to clone envcfg repository
    envcfg_dir = f"{os.getenv('HOME')}/{envcfg_repo.replace(':', '/')}"
    logger.debug("Creating directory for envcfg: %s", envcfg_dir)
    os.makedirs(envcfg_dir, exist_ok=True)

    # Clone envcfg repository
    logger.debug(
        "Cloning envcfg repo: %s, on directory: %s",
        envcfg_repo,
        envcfg_dir,
    )
    try:
        git.Repo.clone_from(f"git@{envcfg_repo}.git", envcfg_dir)
        logger.debug("Repo cloned")
        click.secho("Envcfg repo cloned", fg="green")
    except git.exc.GitError:
        logger.debug(
            "Can not clone as the directory is not empty. Trying to update"
        )
        repo = git.Repo(f"{envcfg_dir}")
        repo.remotes.origin.pull()
        logger.debug("Repo updated")
        click.secho("Envcfg repo updated", fg="green")
    exit()

    # Run envcfg scripts
    default_encoding = locale.getpreferredencoding()
    commands = [
        f"cd {envcfg_dir} && ./debian.sh",
        f"cd {envcfg_dir} && ./install.sh",
    ]
    for command in commands:
        logger.debug("Running command: %s", command)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for line in iter(process.stdout.readline, b""):
            print(line.decode(default_encoding), end="")
        process.wait()


if __name__ == "__main__":
    cli()
