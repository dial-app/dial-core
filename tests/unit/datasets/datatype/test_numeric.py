# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial_core.datasets.datatype import Numeric


@pytest.fixture
def numeric_obj():
    """
    Returns an instance of Numeric.
    """
    return Numeric()


@pytest.mark.parametrize("test_input, expected", [(1, 1), (2, 2)])
def test_process(numeric_obj, test_input, expected):
    assert numeric_obj.process(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [(0, "0"), (1, "1")])
def test_display(numeric_obj, test_input, expected):
    assert numeric_obj.display(test_input) == expected
