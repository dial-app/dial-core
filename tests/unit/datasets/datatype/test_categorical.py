# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial_core.datasets.datatype import Categorical


@pytest.fixture
def categorical_obj():
    """
    Returns an instance of Categorical with categories ["t-shirt", "jeans", "glasses"]
    """

    return Categorical(["t-shirt", "jeans", "glasses"])


# @pytest.mark.parametrize(
#     "test_input, expected", [(1, [0.0, 1.0, 0.0]), (2, [0.0, 0.0, 1.0])]
# )
# def test_process(categorical_obj, test_input, expected):
#     assert categorical_obj.process(test_input).all(expected)


# @pytest.mark.parametrize(
#     "test_input, expected", [(0, "t-shirt"), (1, "jeans"), (2, "glasses")]
# )
# def test_display(categorical_obj, test_input, expected):
#     assert categorical_obj.display(test_input) == expected


# def test_display_exception(categorical_obj):
#     with pytest.raises(IndexError):
#         assert categorical_obj.display(100)
