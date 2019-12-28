# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from dial.datasets import datatype


@pytest.fixture
def categorical_instance():
    """
    Returns an instance of Categorical with categories ["t-shirt", "jeans", "glasses"]
    """

    return datatype.Categorical(["t-shirt", "jeans", "glasses"])


def test_categorical_process(categorical_instance):
    assert categorical_instance.process(1) == 1
