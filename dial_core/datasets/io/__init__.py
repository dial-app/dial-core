# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .dataset_io import (
    CategoricalImgDatasetIO,
    DatasetIO,
    DatasetIOBuilder,
    DatasetIORegistryFactory,
    DatasetIORegistrySingleton,
    NpzDatasetIO,
    NpzDatasetIOBuilder,
    TxtDatasetIO,
    TxtDatasetIOBuilder,
)
from .ttv_sets_io import TTVSetsIO
from .ttv_sets_loader import (
    BostonHousingLoader,
    Cifar10Loader,
    FashionMnistLoader,
    MnistLoader,
    TTVSetsLoader,
)

PredefinedTTVSetsContainer = containers.DynamicContainer()
PredefinedTTVSetsContainer.Mnist = providers.Factory(MnistLoader)
PredefinedTTVSetsContainer.FashionMnist = providers.Factory(FashionMnistLoader)
PredefinedTTVSetsContainer.Cifar10 = providers.Factory(Cifar10Loader)
PredefinedTTVSetsContainer.BostonHousing = providers.Factory(BostonHousingLoader)

__all__ = [
    "DatasetIO",
    "DatasetIOBuilder",
    "NpzDatasetIO",
    "NpzDatasetIOBuilder",
    "TxtDatasetIO",
    "TxtDatasetIOBuilder",
    "CategoricalImgDatasetIO",
    "DatasetIORegistryFactory",
    "DatasetIORegistrySingleton",
    "TTVSetsIO",
    "TTVSetsIO",
    "BostonHousingLoader",
    "Cifar10Loader",
    "FashionMnistLoader",
    "MnistLoader",
    "TTVSetsLoader",
    "PredefinedTTVSetsContainer",
]
