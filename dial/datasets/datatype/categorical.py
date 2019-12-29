# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numbers
from typing import List, Union

import numpy as np
from dial.datasets.datatype import DataType


class Categorical(DataType):
    """
    Represents a Category.

    A Category is a number indexed on an array of strings, each one representing a
    different category.
    """

    def __init__(self, categories: Union[List[str], None] = None):
        super().__init__()

        self.categories = categories

    def process(self, data: Union[list, tuple, np.ndarray, int]) -> int:
        # Sometimes, categorical data can be passed as an array of 1 element
        if isinstance(data, (list, tuple, np.ndarray)):
            return data[0]

        if isinstance(data, numbers.Integral):
            return data

        raise ValueError(
            f"Expected an int or List[int] object, not {type(data).__name__}"
        )

    def display(self, data: int) -> str:
        return self.categories[data]
