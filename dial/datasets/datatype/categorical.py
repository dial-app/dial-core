# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from numbers import Integral
from typing import List, Union

import numpy as np

from .datatype import DataType


class Categorical(DataType):
    """
    Represents a Category.

    A Category is a number indexed on an array of strings, each one representing a
    different category.
    """

    def __init__(self, categories: List[str]):
        super().__init__()

        self.categories = categories

    def process(self, data: Union[list, tuple, np.ndarray, Integral]) -> Integral:
        # Sometimes, categorical data can be passed as an array of 1 element
        if isinstance(data, (list, tuple, np.ndarray)):
            return data[0]

        if isinstance(data, Integral):
            return data

        raise ValueError(
            f"Expected an Integral or List[int] object, not {type(data).__name__}"
        )

    def display(self, data: int) -> str:
        if self.categories is not None:
            return self.categories[data]

        return str(data)
