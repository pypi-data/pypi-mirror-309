"""
INIT MODULE

This module contains notebook init functions.
"""

import subprocess
import os
from jinja2 import Environment, FileSystemLoader

from .exceptions import NotGitRepoError

# useful values
GREEN: str = '\033[0;32m'
NCOL: str = '\033[0m'
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))


def init_labnotebook(name: str) -> None:
    """Create new labnotebook.

    This function creates a new labnotebook by creating a new .labnotebook folder with all the 
    necessary files included.

    :param name: Name of the project.
    :type name: str
    """

    # 1. Go to git root dir
    try:
        git_root: str = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                        universal_newlines = True, stderr=subprocess.PIPE).strip()
    except subprocess.CalledProcessError:
        raise NotGitRepoError("fatal: not a git repository (or any of the parent directories): .git") from None # pylint: disable=line-too-long

    os.chdir(git_root)

    # 2. Get useful variables
    author: str = subprocess.check_output(["git", "config", "--get", "user.name"],
                                          universal_newlines = True).strip()

    # 3. Create config file
    create_config_json(name = name, author = author)

    # 4. Return messages
    print(f"\n{GREEN}Created .labnotebookrc in {git_root}. Please edit it if you want to change labnotebook export behaviour.{NCOL}") # pylint: disable=line-too-long


def create_config_json(name: str, author: str) -> None:
    """Create configuration file.

    This function creates the config.json file of the notebook inside .labnotebook folder.

    :param name: Name of the notebook.
    :type name: str
    :param author: Author of the notebook.
    :type author: str
    """
    environment = Environment(loader=FileSystemLoader(f"{SCRIPT_DIR}/templates/"))
    template = environment.get_template("rc")
    content = template.render(name = name,
                              author = author,
                              script_dir = SCRIPT_DIR)

    with open(".labnotebookrc", mode="w", encoding="utf-8") as config:
        config.write(content)
