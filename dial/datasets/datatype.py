# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Data Types normally used on datasets.
"""

from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from typing import List, Union

import numpy as np

# from PIL import Image


class DataType(metaclass=ABCMeta):
    """
    Abstract class for any data type of a Dataset.
    """

    @abstractmethod
    def process(self, data):
        """
        Return the data after processing given the data type.

        For example, if the DataType is an ImagePath, process() will open the image and
        return the array corresponding to its content.
        """

    @abstractmethod
    def display(self, data):
        """
        Return the display representation of the data.

        For example, for Categorical types this will be the actual category name instead
        of an interger.
        """

    def __str__(self) -> str:
        return type(self).__name__


class ImageArray(DataType):
    """
    Image, represented as an array of int values, each one representing a pixel
    intensity (0-255).

    The array will have shape (W, H), for grayscale images, or (W, H, C), where C
    represents the number of color channels (For RGB images)
    """

    def process(self, data: List[int]) -> List[int]:
        return data

    def display(self, data: List[int]) -> str:
        return str(data)


# class ImagePath(DataType):
#     def process(self, data: str):
#         return Image.open(data).resize(200, 200)
#
#     def display(self, data: str):
#         return str(self.process(data))


class Numeric(DataType):
    """
    Represents a single numeric value.
    """

    def process(self, data: List[int]) -> List[int]:
        return data

    def display(self, data: List[int]) -> str:
        return str(data)


class NumericArray(DataType):
    """
    Represents an array of numeric values (unidimensional)
    """

    def process(self, data: List[int]) -> List[int]:
        return data

    def display(self, data: List[int]) -> str:
        return str(data)


class Categorical(DataType):
    """
    Represents a Category.

    A Category is a number indexed on an array of strings, each one representing a
    different category.
    """

    def __init__(self, categories: Union[List[str], None] = None):
        super().__init__()

        self.categories = categories

    def process(self, data: Union[List[int], int]) -> int:
        # Sometimes, categorical data can be passed as an array of 1 element
        if isinstance(data, (Sequence, np.ndarray)):
            return data[0]

        return data

    def display(self, data: int) -> str:
        return self.categories[data]
