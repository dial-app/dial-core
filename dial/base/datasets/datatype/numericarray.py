# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np

from .datatype import DataType


class NumericArray(DataType):
    """
    Represents an array of numeric values (unidimensional)
    """

    def process(self, data: "np.ndarray") -> "np.ndarray":
        return data

    def display(self, data: "np.ndarray") -> str:
        return np.array2string(data, precision=4, suppress_small=True, separator=", ")
