"""PYLABNOTEBOOK
This module is the cli module where cli functionality of pylabnotebook is defined.
"""

# pylint: disable=line-too-long

import argparse
import sys

from .version import __version__
from .init import init_labnotebook
from .export import export_labnotebook
from .exceptions import NotGitRepoError, NotInitializedError, OutputAlreadyExistsError, EmptyHisoryError

def main():
    """Main cli function handler.

    This function is the main function of the module, which handles command line input values to run
    the different functions of the labnotebook.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Lab Notebook Tool")
    parser.add_argument('--version', action = 'version', version = '%(prog)s ' + __version__,
                        help = "Show package version")

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest = "command")

    init_parser: argparse.ArgumentParser = subparsers.add_parser("init",
                                                                 help = "Init labnotebook by creating .labnotebookrc in git root folder.") # pylint: disable=line-too-long
    init_parser.add_argument("-n", "--name", required = True,
                               help="Name of the lab notebook. If the name should contain more words, wrap them into quotes") # pylint: disable=line-too-long

    export_parser: argparse.ArgumentParser = subparsers.add_parser("export", help = "Export lab notebook to an html file") # pylint: disable=line-too-long
    export_parser.add_argument("-o", "--output", required = True,
                               help = "Path/name of the output HTML file")
    export_parser.add_argument("-f", "--force",
                               help = "Force the overwriting of the output file if already present",
                               default = False, action = "store_true")
    export_parser.add_argument("--no-link", default = False, action = "store_true",
                               help = "Disable links to analyses files.") # pylint: disable=line-too-long

    args = parser.parse_args()

    if args.command == "init":
        try:
            init_labnotebook(args.name)
        except NotGitRepoError as e:
            print(e)
            sys.exit(128)
    elif args.command == "export":
        try:
            export_labnotebook(args.output, args.force, not args.no_link)
        except NotGitRepoError as e:
            print(e)
            sys.exit(128)
        except NotInitializedError as e:
            print(e)
            sys.exit(2)
        except OutputAlreadyExistsError as e:
            print(e)
            sys.exit(17)
        except EmptyHisoryError as e:
            print(e)
            sys.exit(5)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
