# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Functions to check that python versions, libraries... used by the program are correct.
"""

import importlib
import sys
from typing import List, Tuple

from dial.utils import log

LOGGER = log.get_logger(__name__)


def check_python_version():
    """
    Check if Python version installed is correct.
    """
    # Check correct python version
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise SystemError("Must use Python 3.6 or newer.")

    LOGGER.debug("Python Version: %s", sys.version)


def check_module_installed(module_name: str):
    """
    Check if PySide2 version installed is correct.
    """
    spec = importlib.util.find_spec(module_name)

    if spec is None:
        raise ImportError(
            f"{module_name} module not found!\n\nPlease use "
            f'"pip install --user {module_name}" to install it.'
        )

    LOGGER.debug("%s module found (%s)", spec.name, spec.origin)


def check_required_modules(requirements: List[Tuple[str, str]]):
    """
    Check if the required modules are installed.
    """
    # Warning: Pillow module is actually imported as "PIL", so we have to change its
    # name before checking it
    # Same with "dependency-injector", which is imported name has an underscore
    # (dependency_injector)
    module_imported_name = {
        "Pillow": "PIL",
        "dependency-injector": "dependency_injector",
    }

    # Iterate through each module
    for module_name, _ in requirements:
        try:
            check_module_installed(module_imported_name[module_name])
        except KeyError:
            check_module_installed(module_name)
