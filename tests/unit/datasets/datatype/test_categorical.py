# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np
import pytest

from dial_core.datasets.datatype import Categorical


@pytest.fixture
def categorical_obj():
    """
    Returns an instance of Categorical with categories ["t-shirt", "jeans", "glasses"]
    """

    return Categorical(["t-shirt", "jeans", "glasses"])


@pytest.mark.parametrize("test_input, expected", [(1, [0, 1, 0]), (2, [0, 0, 1])])
def test_process(categorical_obj, test_input, expected):
    assert categorical_obj.process(test_input).tolist() == expected


def test_process_out_of_bounds(categorical_obj):
    with pytest.raises(IndexError):
        categorical_obj.process(100)


@pytest.mark.parametrize(
    "test_input, expected", [(0, "t-shirt"), (1, "jeans"), (2, "glasses")]
)
def test_display(categorical_obj, test_input, expected):
    assert categorical_obj.display(test_input) == expected


def test_display_out_of_bounds(categorical_obj):
    with pytest.raises(IndexError):
        categorical_obj.display(100)


def test_convert_to_expected_format(categorical_obj):
    assert categorical_obj.convert_to_expected_format(0) == 0
    assert categorical_obj.convert_to_expected_format("jeans") == 1
    assert categorical_obj.convert_to_expected_format("2") == 2
    assert categorical_obj.convert_to_expected_format([1]) == 1
    assert categorical_obj.convert_to_expected_format([0, 0, 1, 0]) == 2
    assert categorical_obj.convert_to_expected_format(np.array([0, 1, 0]))

    with pytest.raises(ValueError):
        # Invalid category
        assert categorical_obj.convert_to_expected_format("not-exists")

    with pytest.raises(ValueError):
        # Out of range
        assert categorical_obj.convert_to_expected_format(40)

    with pytest.raises(ValueError):
        assert categorical_obj.convert_to_expected_format([0, 0, 0, 0, 1, 0])

    with pytest.raises(ValueError):
        assert categorical_obj.convert_to_expected_format(None)


def test_str(categorical_obj):
    assert str(categorical_obj) == "Categorical"
