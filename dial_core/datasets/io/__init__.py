# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .ttv_sets_io import TTVSetsIO
from .ttv_sets_io_format import NpzFormat, TTVSetsIOFormat, TxtFormat
from .ttv_sets_loader import (
    BostonHousingLoader,
    Cifar10Loader,
    FashionMnistLoader,
    MnistLoader,
    TTVSetsLoader,
)

TTVSetsFormatsContainer = containers.DynamicContainer()
TTVSetsFormatsContainer.NpzFormat = providers.Factory(NpzFormat)
TTVSetsFormatsContainer.TxtFormat = providers.Factory(TxtFormat)

PredefinedTTVSetsContainer = containers.DynamicContainer()
PredefinedTTVSetsContainer.Mnist = providers.Factory(MnistLoader)
PredefinedTTVSetsContainer.FashionMnist = providers.Factory(FashionMnistLoader)
PredefinedTTVSetsContainer.Cifar10 = providers.Factory(Cifar10Loader)
PredefinedTTVSetsContainer.BostonHousing = providers.Factory(BostonHousingLoader)

__all__ = [
    "TTVSetsLoader",
    "TTVSetsIO",
    "TTVSetsIOFormat",
    "TTVSetsFormatsContainer",
    "PredefinedTTVSetsContainer",
    "NpzFormat",
    "TxtFormat",
]
