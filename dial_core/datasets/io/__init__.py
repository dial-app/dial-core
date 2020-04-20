# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .dataset_io import DatasetIO
from .dataset_io_format import DatasetIOFormat, NpzFormat, TxtFormat

DatasetFormatsContainer = containers.DynamicContainer()
DatasetFormatsContainer.NpzFormat = providers.Factory(NpzFormat)
DatasetFormatsContainer.TxtFormat = providers.Factory(TxtFormat)

__all__ = [
    "DatasetIO",
    "DatasetIOFormat",
    "DatasetFormatsContainer",
    "NpzIOFormat",
]
