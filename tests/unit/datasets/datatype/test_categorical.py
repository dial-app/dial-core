# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from dial.datasets.datatype import Categorical


@pytest.fixture
def categorical_obj():
    """
    Returns an instance of Categorical with categories ["t-shirt", "jeans", "glasses"]
    """

    return Categorical(["t-shirt", "jeans", "glasses"])


@pytest.mark.parametrize("test_input, expected", [(1, 1), ([5], 5)])
def test_process(categorical_obj, test_input, expected):
    assert categorical_obj.process(test_input) == expected


@pytest.mark.parametrize("test_input", ["string", 2.3])
def test_process_invalid_values(categorical_obj, test_input):
    with pytest.raises(ValueError):
        assert categorical_obj.process(test_input)


@pytest.mark.parametrize(
    "test_input, expected", [(0, "t-shirt"), (1, "jeans"), (2, "glasses")]
)
def test_display(categorical_obj, test_input, expected):
    assert categorical_obj.display(test_input) == expected


def test_display_exception(categorical_obj):
    with pytest.raises(IndexError):
        assert categorical_obj.display(100)
