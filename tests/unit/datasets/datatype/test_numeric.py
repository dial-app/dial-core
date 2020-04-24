# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest


@pytest.mark.parametrize("test_input, expected", [(1, 1), (2, 2)])
def test_process(numeric_obj, test_input, expected):
    assert numeric_obj.process(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [(0, "0"), (1, "1")])
def test_display(numeric_obj, test_input, expected):
    assert numeric_obj.display(test_input) == expected


def test_convert_to_expected_format(numeric_obj):
    assert numeric_obj.convert_to_expected_format(5) == 5


def test_pickable(numeric_obj):
    obj = pickle.dumps(numeric_obj)
    pickle.loads(obj)
