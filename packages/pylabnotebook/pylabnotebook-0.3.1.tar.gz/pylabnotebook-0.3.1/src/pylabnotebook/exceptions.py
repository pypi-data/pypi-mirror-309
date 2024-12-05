"""
EXCEPTIONS MODULE

Here, all custome exceptions are defined.
"""

# pylint: disable=line-too-long

class NotGitRepoError(Exception):
    """Exception class used when no .git repository is found.
    """

class NotInitializedError(Exception):
    """Exception class used when export is run prior to init."""

class OutputAlreadyExistsError(Exception):
    """Exception class used when output of export is already present and export is not run with force."""

class EmptyHisoryError(Exception):
    """Exception class used when git history is empty."""
