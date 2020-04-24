# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np

from .datatype import DataType


class NumericArray(DataType):
    """The NumericArray class represents an unidimensional array of numeric values."""

    def process(self, data: "np.ndarray") -> "np.ndarray":
        """Returns the data as it is. Doesn't need any processing."""
        return data

    def display(self, data: "np.ndarray") -> str:
        """Returns `data` as a string representation."""
        return np.array2string(data, precision=4, suppress_small=True, separator=", ")

    def convert_to_expected_format(self, data: "np.ndarray") -> "np.ndarray":
        """Doesn't do any transformation. Expects data to be passed correctly."""
        return np.array(data)

    def __reduce__(self):
        return (NumericArray, (), super().__getstate__())
