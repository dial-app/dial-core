# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Modules related to Datasets, types and dataset loading.
"""

from .dataset import Dataset
from .dataset_loader import (
    BostonHousingLoader,
    Cifar10Loader,
    DatasetLoader,
    FashionMnistLoader,
    MnistLoader,
)

PREDEFINED_DATASETS = {
    "mnist": MnistLoader(),
    "fashion-mnist": FashionMnistLoader(),
    "cifar10": Cifar10Loader(),
    "boston-housing": BostonHousingLoader(),
}

__all__ = [
    "Dataset",
    "PREDEFINED_DATASETS",
    "BostonHousingLoader",
    "Cifar10Loader",
    "FashionMnistLoader",
    "MnistLoader",
    "DatasetLoader",
]
