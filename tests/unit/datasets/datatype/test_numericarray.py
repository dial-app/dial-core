# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from dial.datasets.datatype import NumericArray


@pytest.fixture
def numericarray_obj():
    """
    Returns an instance of NumericArray.
    """
    return NumericArray()


@pytest.mark.parametrize("test_input, expected", [([1, 2, 3], [1, 2, 3])])
def test_process(numericarray_obj, test_input, expected):
    assert numericarray_obj.process(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [([1, 2], "[1, 2]")])
def test_display(numericarray_obj, test_input, expected):
    assert numericarray_obj.display(test_input) == expected
