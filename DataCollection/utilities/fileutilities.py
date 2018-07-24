# coding=utf-8

"""
Helper functions for files and directories.
"""

from os import makedirs
from os.path import exists


def check_directory(path: str) -> None:
    """
    Helper function to make sure that a directory exists at a path, if not create one.
    :param path:
    """
    if not exists(path):
        makedirs(path)
