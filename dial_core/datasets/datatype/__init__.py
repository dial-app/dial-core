# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
DataTypes used by the datasets
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .categorical import Categorical
from .datatype import DataType
from .imagearray import ImageArray
from .numeric import Numeric
from .numericarray import NumericArray

DataTypeContainer = containers.DynamicContainer()
DataTypeContainer.Categorical = providers.Factory(Categorical)
DataTypeContainer.ImageArray = providers.Factory(ImageArray)
DataTypeContainer.Numeric = providers.Factory(Numeric)
DataTypeContainer.NumericArray = providers.Factory(NumericArray)

__all__ = [
    "Categorical",
    "DataType",
    "ImageArray",
    "Numeric",
    "NumericArray",
    "DataTypeContainer",
]
