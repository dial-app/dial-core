# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

from tensorflow import keras

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

    def process(self, data: int) -> List[int]:
        return keras.utils.to_categorical(data, len(self.categories))

    def display(self, data: int) -> str:
        return self.categories[data]
