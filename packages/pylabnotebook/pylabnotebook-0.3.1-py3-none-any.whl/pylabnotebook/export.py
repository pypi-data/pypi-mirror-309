"""
EXPORT MODULE

This module contains notebook export functions.
"""

# pylint: disable=line-too-long

import subprocess
import os
import yaml
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from .exceptions import NotGitRepoError, NotInitializedError, OutputAlreadyExistsError, EmptyHisoryError

# useful values
RED: str = '\033[0;31m'
NCOL: str = '\033[0m'
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))

def export_labnotebook(output_file: str, force: bool, link: bool) -> None:
    """Export labnotebook to html.

    This function exports the labnotebook into a single html file ready to read and share.

    :param output_file: path of the file to create
    :type output_file: str
    :param force: whether to force the overwriting of output_file if exists.
    :type force: bool
    :param link: whether to create links to analysis files in analysis files bullet list. These links can be used to open the analysis files directly from the notebook. # pylint: disable=line-too-long
    :type link: bool

    """

    # 1. Go to git root dir
    try:
        git_root: str = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                        universal_newlines = True, stderr=subprocess.PIPE).strip()
    except subprocess.CalledProcessError:
        raise NotGitRepoError("fatal: not a git repository (or any of the parent directories): .git") from None

    os.chdir(git_root)

    # 2. Check for .labnotebookrc
    if not os.path.exists(".labnotebookrc"):
        raise NotInitializedError(f"{RED}Error: There is no .labnotebookrc file in git repository root folder. Please, run labnotebook create -n <name_of_the_project>{NCOL}")

    with open(".labnotebookrc", "r", encoding = 'utf8') as config_file:
        config: dict = yaml.safe_load(config_file)

    # 3. Check if file already exists and force is False
    if os.path.exists(output_file) and not force:
        raise OutputAlreadyExistsError(f"{RED}Error: {output_file} already exists. Use -f/--force to overwrite it.{NCOL}")

    # 5. Get list of commits sha
    sha_list: list[str] = get_sha_list(config.get("REVERSE_HISTORY"))

    # 6. Get info about each commit
    commits_info: dict = {sha: get_commit_info(sha, analysis_ext = config.get('ANALYSIS_EXT'),
                                               excluded_patterns = config.get('ANALYSIS_IGNORE')) for sha in sha_list}

    # 7. Read style.css
    with open(config.get('LAB_CSS'), 'r', encoding='utf-8') as css_file:
        style_css = css_file.read()

    environment = Environment(loader=FileSystemLoader(f"{SCRIPT_DIR}/templates/"))
    template = environment.get_template("base.html")
    content = template.render(config = config,
                              create_date = datetime.today().strftime('%Y-%m-%d'),
                              link = link,
                              commits_info = commits_info,
                              style_css = style_css)

    with open(output_file, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"Notebook succesfully exported to {output_file}.")


def get_sha_list(reverse_history: bool) -> list[str]:
    """Get sha list.

    This functions returns a list of commits sha (from oldest to newest) that have not been already 
    included in the notebook.

    :param reverse_history: Whether commits should be returned from first to last.
    :type reverse_history: bool
    :return: list of the commits not included in the notebook since last_commit.
    :rtype: list[str]
    """

    # 1. Get list of all commits
    git_command = ["git", "log", "--pretty=format:%h"]
    if reverse_history:
        git_command.append("--reverse")

    try:
        git_sha: list[str] = subprocess.check_output(git_command, text = True, stderr=subprocess.PIPE).split('\n')
    except subprocess.CalledProcessError:
        raise EmptyHisoryError(f"{RED}Error: Git history is empty{NCOL}") from None

    return git_sha


def get_commit_info(commit_sha: str, analysis_ext: list[str], excluded_patterns: list[str]) -> dict:
    """Get commit info.

    This function returns a dictionary of the information about the commit specified in commit_sha. 
    These info are: date, author, title, message, changed files and analysis_files (based on both
    analysis_ext and excluded_patterns).

    :param commit_sha: sha of the commit of interest.
    :type commit_sha: str
    :param analysis_ext: list of the file extensions used as reference for analysis files.
    :type analysis_ext: list[str]
    :param excluded_patterns: list of the pattern to be excluded from the analysis files.
    :type excluded_patterns: list[str]
    
    :return: information about the commit specified in commit_sha: date, author, title, message, 
    changed files and analysis_files (based on both analysis_ext and excluded_patterns).
    :rtype: dict
    """
    date, author, title = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%cs%n%an%n%s', commit_sha], text = True).strip().split('\n')

    # Get message and replace newlines with html breaks
    message: str = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%b', commit_sha], text=True).strip()
    pattern: str = r"(\.|:|!|\?)\n"
    replacement: str = r"\1<br>\n"
    message = re.sub(pattern, replacement, message).replace('\n\n', '\n<br>\n')

    changed_files: list[str] = subprocess.check_output(['git', 'show', '--pretty=%n', '--name-status', commit_sha], text=True).strip().split('\n')
    if changed_files == ['']:
        changed_files = {}
    else:
        changed_files: dict = {file.split('\t')[1] : file.split('\t')[0] for file in changed_files}
    analysis_files: list[str] = [key for key, _ in changed_files.items()
                                 if any(ext in key for ext in analysis_ext) and
                                 os.path.isfile(key) and not
                                 any(re.search(pattern, key) for pattern in excluded_patterns)]
    commit_info: dict = {'date': date,
                         'author': author,
                         'title': title,
                         'message': message,
                         'changed_files': changed_files,
                         'analysis_files': analysis_files}

    return commit_info
