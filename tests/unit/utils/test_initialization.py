# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


import sys
from unittest.mock import patch

import pytest

from dial.utils import initialization


@patch.object(sys, "version_info", [3, 6])
def test_check_python_version():
    initialization.check_python_version()


@patch.object(sys, "version_info", [3, 4])
def test_check_python_version_invalid():
    with pytest.raises(SystemError):
        initialization.check_python_version()


def test_required_modules():
    with pytest.raises(ImportError):
        initialization.check_required_modules([("Inexistent", "0.0.0")])
