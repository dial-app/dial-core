# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np
import pytest

from dial_core.datasets.datatype import ImageArray


@pytest.fixture
def imagearray_obj():
    """
    Returns an instance of ImageArray.
    """
    return ImageArray()


@pytest.mark.parametrize(
    "test_input, expected",
    [(np.array([1, 2, 3]), np.array([1 / 255, 2 / 255, 3 / 255]))],
)
def test_process(imagearray_obj, test_input, expected):
    assert np.alltrue(imagearray_obj.process(test_input) == expected)


@pytest.mark.parametrize("input_output", [(np.array([1, 2, 3]))])
def test_display(imagearray_obj, input_output):
    assert np.alltrue(imagearray_obj.display(input_output) == input_output)
