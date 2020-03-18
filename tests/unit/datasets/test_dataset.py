# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import numpy as np
import pytest

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import Numeric

np.random.seed(0)


@pytest.fixture
def empty_dataset():
    return Dataset()


@pytest.fixture
def simple_numeric_dataset():
    return Dataset(
        x_data=np.array([1, 2, 3, 4]),
        y_data=np.array([10, 20, 30, 40]),
        x_type=Numeric(),
        y_type=Numeric(),
    )


def test_empty_dataset(empty_dataset):
    x, y = empty_dataset.head(10)

    assert len(x) == 0
    assert len(y) == 0


def test_shuffled(simple_numeric_dataset):
    simple_numeric_dataset.shuffled = True
    assert simple_numeric_dataset.shuffled is True

    x, y = simple_numeric_dataset.head(2)

    assert x.tolist() == [3, 4]
    assert y.tolist() == [30, 40]


def test_head(simple_numeric_dataset):
    x, y = simple_numeric_dataset.head(2)

    assert x.tolist() == [1, 2]
    assert y.tolist() == [10, 20]


def test_head_with_more_elements(simple_numeric_dataset):
    x, y = simple_numeric_dataset.head(10000)

    assert x.tolist() == [1, 2, 3, 4]
    assert y.tolist() == [10, 20, 30, 40]


def test_items(simple_numeric_dataset):
    x, y = simple_numeric_dataset.items(1, 3)

    assert x.tolist() == [2, 3]
    assert y.tolist() == [20, 30]


def test_items_with_more_elements(simple_numeric_dataset):
    x, y = simple_numeric_dataset.items(1, 2000)

    assert x.tolist() == [2, 3, 4]
    assert y.tolist() == [20, 30, 40]


def test_get_batch(simple_numeric_dataset):
    simple_numeric_dataset.batch_size = 2

    bx, by = simple_numeric_dataset[0]

    assert bx.tolist() == [1, 2]
    assert by.tolist() == [10, 20]

    bx, by = simple_numeric_dataset[1]

    assert bx.tolist() == [3, 4]
    assert by.tolist() == [30, 40]


def test_delete_rows(simple_numeric_dataset):
    simple_numeric_dataset.delete_rows(0)

    x, y = simple_numeric_dataset.head(3)

    assert x.tolist() == [2, 3, 4]
    assert y.tolist() == [20, 30, 40]

    simple_numeric_dataset.delete_rows(1, 20)

    x, y = simple_numeric_dataset.head(3)

    assert x.tolist() == [2]
    assert y.tolist() == [20]


def test_get_irregular_batches(simple_numeric_dataset):
    simple_numeric_dataset.batch_size = 3

    bx, by = simple_numeric_dataset[0]

    assert bx.tolist() == [1, 2, 3]
    assert by.tolist() == [10, 20, 30]

    bx, by = simple_numeric_dataset[1]

    assert bx.tolist() == [4]
    assert by.tolist() == [40]


def test_pickable(simple_numeric_dataset):
    obj = pickle.dumps(simple_numeric_dataset)
    pickle.loads(obj)
