# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from .datatype import DataType

if TYPE_CHECKING:
    import numpy as np


class NumericArray(DataType):
    """
    Represents an array of numeric values (unidimensional)
    """

    def process(self, data: "np.ndarray") -> "np.ndarray":
        return data

    def display(self, data: "np.ndarray") -> str:
        return np.array2string(data, precision=4, suppress_small=True, separator=", ")
