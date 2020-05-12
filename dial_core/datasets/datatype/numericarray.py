# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Callable, List

import dependency_injector.providers as providers
import numpy as np

from .datatype import DataType, DataTypeContainer


class NumericArray(DataType):
    """The NumericArray class represents an unidimensional array of numeric values."""

    def __init__(self):
        super().__init__()

        self.transformations: List[Callable] = []

    def process(self, data: "np.ndarray") -> "np.ndarray":
        """Returns the data as it is. Doesn't need any processing."""
        return self._apply_transformations(data)

    def display(self, data: "np.ndarray") -> str:
        """Returns `data` as a string representation."""
        return np.array2string(data, precision=4, suppress_small=True, separator=", ")

    def convert_to_expected_format(self, data: "np.ndarray") -> "np.ndarray":
        """Doesn't do any transformation. Expects data to be passed correctly."""
        return np.array(data)

    def __reduce__(self):
        return (NumericArray, (), super().__getstate__())


DataTypeContainer.NumericArray = providers.Factory(NumericArray)
