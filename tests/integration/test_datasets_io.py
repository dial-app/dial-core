# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

import numpy as np

from dial_core.datasets import Dataset, DatasetsContainer, DatasetExporter
from dial_core.datasets.datatype import Numeric, NumericArray


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
    dc = DatasetsContainer(name="TestContainer", train=train_dataset, test=test_dataset)

    dc_exporter = DatasetExporter()
    dc_exporter.export(".", dc)

    dc_imported = dc_exporter.import_dataset("./TestContainer")
    print(dc_imported.train.items())
