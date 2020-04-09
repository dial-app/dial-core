# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List, Union

import numpy as np
from tensorflow import keras

from .datatype import DataType


class Categorical(DataType):
    """
    Represents a Category.

    A Category is a number indexed on an array of strings, each one representing a
    different category.
    """

    def __init__(self, categories: List[str] = []):
        super().__init__()

        self.is_editable = True

        self.categories = categories

    def process(self, data: int) -> List[int]:
        return keras.utils.to_categorical(data, len(self.categories))

    def display(self, data: int) -> str:
        return self.categories[data]

    def convert_to_expected_format(self, data: Union[str, int]) -> int:
        """
        Tries to transform an input value to the value expected to be stored on the
        dataset.

        Examples:
            categories => ["foo", "bar"]

            convert_to_expected_format(0) == 0
            convert_to_expected_format(3) == ValueError     # Out of range
            convert_to_expected_format("1") == 1
            convert_to_expected_format("5") == ValueError   # Out of range
            convert_to_expected_format("bar") == 1
            convert_to_expected_format("hue") == ValueError # Not a valid category

        Raises:
            ValueError: If the data can't be converted.
        """

        if isinstance(data, str):
            try:
                data_as_int = int(data)
            except ValueError:
                data_as_int = self.categories.index(data)

        elif isinstance(data, int):
            data_as_int = int(data)

        elif isinstance(data, (list, tuple, np.ndarray)):
            data_as_int = np.argmax(data)

        else:
            raise ValueError

        if data_as_int >= 0 and data_as_int < len(self.categories):
            return data_as_int

        raise ValueError
