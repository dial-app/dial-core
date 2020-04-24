# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np
import pytest

from dial_core.datasets import Dataset, TTVSets
from dial_core.datasets.datatype import Numeric


@pytest.fixture
def simple_numeric_dataset():
    return Dataset(
        x_data=np.array([1, 2, 3, 4]),
        y_data=np.array([10, 20, 30, 40]),
        x_type=Numeric(),
        y_type=Numeric(),
    )


@pytest.fixture
def ttv_sets(simple_numeric_dataset):
    return TTVSets(
        "TTVSets",
        train=simple_numeric_dataset,
        test=simple_numeric_dataset,
        validation=None,
    )


def test_ttv_sets_to_dict(ttv_sets):
    dc = ttv_sets.to_dict()

    assert dc["dataset"]["name"] == ttv_sets.name
    assert dc["train"]["x_type"] == str(ttv_sets.train.x_type)
    assert dc["train"]["y_type"] == str(ttv_sets.train.y_type)
    assert dc["test"]["x_type"] == str(ttv_sets.test.x_type)
    assert dc["test"]["y_type"] == str(ttv_sets.test.y_type)
    assert dc["validation"] == {}
