# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import sys
from unittest.mock import patch

import pytest

from dial_core.utils import initialization


@patch.object(sys, "version_info", [3, 6])
def test_check_python_version():
    initialization.check_python_version()


@patch.object(sys, "version_info", [3, 4])
def test_check_python_version_invalid():
    with pytest.raises(SystemError):
        initialization.check_python_version()


@patch.object(sys, "version_info", [3, 6])
def test_initialize():
    initialization.initialize(initialization.parse_args([]))


@patch.object(sys, "version_info", [3, 4])
def test_initialize_error():
    with pytest.raises(SystemError):
        initialization.initialize(initialization.parse_args([]))


def test_parser_debug():
    parsed_args = initialization.parse_args([])

    assert not parsed_args.debug

    parsed_args = initialization.parse_args(["-d"])

    assert parsed_args.debug

    parsed_args = initialization.parse_args(["--debug"])

    assert parsed_args.debug


def test_parser_loglevel():
    parsed_args = initialization.parse_args([])

    assert parsed_args.loglevel == "info"

    parsed_args = initialization.parse_args(["-l", "critical"])

    assert parsed_args.loglevel == "critical"

    with pytest.raises(SystemExit):
        parsed_args = initialization.parse_args(["-l", "THIS_VALUE_DOESNT_EXIST"])
