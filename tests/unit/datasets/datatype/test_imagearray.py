# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import numpy as np
import pytest


@pytest.mark.parametrize(
    "test_input, expected",
    [(np.array([1, 2, 3]), np.array([1 / 255, 2 / 255, 3 / 255]))],
)
def test_process(imagearray_obj, test_input, expected):
    assert np.alltrue(imagearray_obj.process(test_input) == expected)


@pytest.mark.parametrize("input_output", [(np.array([1, 2, 3]))])
def test_display(imagearray_obj, input_output):
    assert np.alltrue(imagearray_obj.display(input_output) == input_output)


def test_convert_to_expected_format(imagearray_obj):
    assert imagearray_obj.convert_to_expected_format([0, 5, 12]).tolist() == [0, 5, 12]


def test_pickable(imagearray_obj):
    obj = pickle.dumps(imagearray_obj)
    pickle.loads(obj)
