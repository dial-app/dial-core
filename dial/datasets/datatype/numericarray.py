# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

import numpy as np
from dial.datasets.datatype import DataType


class NumericArray(DataType):
    """
    Represents an array of numeric values (unidimensional)
    """

    def process(self, data: List[int]) -> List[int]:
        return data

    def display(self, data: List[int]) -> str:
        return np.array2string(data, precision=4, suppress_small=True)
