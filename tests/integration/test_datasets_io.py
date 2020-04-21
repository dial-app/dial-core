# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np
import pytest

from dial_core.datasets import Dataset, TTVSets
from dial_core.datasets.datatype import Numeric, NumericArray
from dial_core.datasets.io import TTVSetsFormatsContainer, TTVSetsIO


@pytest.fixture
def train_dataset():
    return Dataset(
        x_data=np.array(
            [np.array([1, 1, 1]), np.array([2, 2, 2]), np.array([3, 3, 3])]
        ),
        y_data=np.array([1, 2, 3]),
        x_type=NumericArray(),
        y_type=Numeric(),
    )


@pytest.fixture
def test_dataset():
    return Dataset(
        x_data=np.array(
            [np.array([1, 1, 1]), np.array([2, 2, 2]), np.array([3, 3, 3])]
        ),
        y_data=np.array([1, 2, 3]),
        x_type=NumericArray(),
        y_type=Numeric(),
    )


def test_datasets_io(train_dataset, test_dataset):
    dg = TTVSets(name="TestContainer", train=train_dataset, test=test_dataset)

    TTVSetsIO.save(TTVSetsFormatsContainer.NpzFormat(), ".", dg)
    load_dg = TTVSetsIO.load("./TestContainer", TTVSetsFormatsContainer)

    for dataset, loaded_dataset in zip(
        [dg.train, dg.test], [load_dg.train, load_dg.test],
    ):
        x, y = dataset.items()
        xl, ly = loaded_dataset.items()

        assert x.tolist() == xl.tolist()

    assert load_dg.validation is None
