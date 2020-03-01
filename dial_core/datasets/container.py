# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .dataset_loader import (
    BostonHousingLoader,
    Cifar10Loader,
    FashionMnistLoader,
    MnistLoader,
)

PredefinedDatasetLoaders = containers.DynamicContainer()

PredefinedDatasetLoaders.Mnist = providers.Factory(MnistLoader)
PredefinedDatasetLoaders.FashionMnist = providers.Factory(FashionMnistLoader)
PredefinedDatasetLoaders.Cifar10 = providers.Factory(Cifar10Loader)
PredefinedDatasetLoaders.BostonHousing = providers.Factory(BostonHousingLoader)
