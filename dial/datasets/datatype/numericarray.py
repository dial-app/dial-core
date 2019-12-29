# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets.datatype import DataType
from typing import List


class NumericArray(DataType):
    """
    Represents an array of numeric values (unidimensional)
    """

    def process(self, data: List[int]) -> List[int]:
        return data

    def display(self, data: List[int]) -> str:
        return str(data)
