# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .ttv_sets_io import TTVSetsIO
from .ttv_sets_io_format import TTVSetsIOFormat, NpzFormat, TxtFormat

TTVSetsFormatsContainer = containers.DynamicContainer()
TTVSetsFormatsContainer.NpzFormat = providers.Factory(NpzFormat)
TTVSetsFormatsContainer.TxtFormat = providers.Factory(TxtFormat)

__all__ = [
    "TTVSetsIO",
    "TTVSetsIOFormat",
    "TTVSetsFormatsContainer",
    "NpzFormat",
    "TxtFormat"
]
