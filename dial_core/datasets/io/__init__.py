# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .dataset_io import CategoricalImgDatasetIO, DatasetIO, NpzDatasetIO, TxtDatasetIO
from .ttv_sets_io import TTVSetsIO
from .ttv_sets_loader import (
    BostonHousingLoader,
    Cifar10Loader,
    FashionMnistLoader,
    MnistLoader,
    TTVSetsLoader,
)

DatasetIOContainer = containers.DynamicContainer()
DatasetIOContainer.Npz = providers.Factory(NpzDatasetIO)
DatasetIOContainer.Txt = providers.Factory(TxtDatasetIO)
DatasetIOContainer.CategoricalImg = providers.Factory(CategoricalImgDatasetIO)

PredefinedTTVSetsContainer = containers.DynamicContainer()
PredefinedTTVSetsContainer.Mnist = providers.Factory(MnistLoader)
PredefinedTTVSetsContainer.FashionMnist = providers.Factory(FashionMnistLoader)
PredefinedTTVSetsContainer.Cifar10 = providers.Factory(Cifar10Loader)
PredefinedTTVSetsContainer.BostonHousing = providers.Factory(BostonHousingLoader)

__all__ = [
    "DatasetIO",
    "NpzDatasetIO",
    "TxtDatasetIO",
    "CategoricalImgDatasetIO",
    "DatasetIOContainer" "TTVSetsIO",
    "TTVSetsIO",
    "BostonHousingLoader",
    "Cifar10Loader",
    "FashionMnistLoader",
    "MnistLoader",
    "TTVSetsLoader",
    "PredefinedTTVSetsContainer",
]
