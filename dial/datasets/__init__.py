# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Modules related to Datasets, types and dataset loading.
"""

from .dataset import Dataset
from .predefined_dataset_loader import (
    PREDEFINED_DATASETS,
    BostonHousingLoader,
    Cifar10Loader,
    FashionMnistLoader,
    MnistLoader,
    PredefinedDatasetLoader,
)

__all__ = [
    "Dataset",
    "PREDEFINED_DATASETS",
    "BostonHousingLoader",
    "Cifar10Loader",
    "FashionMnistLoader",
    "MnistLoader",
    "PredefinedDatasetLoader",
]
