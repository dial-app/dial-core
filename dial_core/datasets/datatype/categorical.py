# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Callable, List, Union

import dependency_injector.providers as providers
import numpy as np
from tensorflow import keras

from .datatype import DataType, DataTypeContainer


class Categorical(DataType):
    """
    The Categorical class represents a datatype that is a Category.

    This type also has a list of strings, each one representing a category
    (also named class).

    On memory, categories are stored as an interger, each one representing an index on
    the `categories` array.

    When categories are __processed__, they are transformed to the "one-hot-encoding"
    format (see `self.process` for more information).

    Attributes:
        categories: List of all the categories used by this datatype.

    Examples:
        for categories = ["a", "b", "c"]:

        A category can be represented using any of the following formats:
        "a" == [1, 0, 0] == 0 == [0]
        "b" == [0, 1, 0] == 1 == [1]
        "c" == [0, 0, 1] == 2 == [2]
    """

    def __init__(self, categories: List[str] = []):
        super().__init__()

        self.is_editable = True

        self.categories = categories

        self.transformations: List[Callable] = []

    def process(self, data: int) -> List[int]:
        """Returns `data` on the one-hot-encoding format.

        `data` must be provided as an interger representing the index of the category,
        and it is transformed to the one-hot-encoding format.

        Examples:
            For categories = ["a", "b", "c"]
            data = 0   Output: [1, 0, 0]
            data = 1   Output: [0, 1, 0]
            data = 2   Output: [0, 0, 1]
            data = 100 Output: Raises IndexError

        Raises:
            IndexError: if `data` is out of bounds of the `categories` array.
        """
        return self._apply_transformations(
            keras.utils.to_categorical(data, len(self.categories))
        )

    def display(self, data: int) -> str:
        """Returns `data` as the corresponding name of the category.

        Examples:
            For categories = ["a", "b", "c"]
            data = 0   Output: "a"
            data = 1   Output: "b"
            data = 2   Output: "c"
            data = 100 Output: Raises IndexError

        Raises:
            IndexError: if `data` is out of bounds of the `categories` array.
        """
        return self.categories[data]

    def convert_to_expected_format(self, data: Union[str, int, list]) -> int:
        """
        Tries to transform an input value to the value expected to be stored on the
        dataset.

        Input values can be passed as:
            * an int: 1
            * a string representing an int: "1"
            * a len 1 list representing an int: [1]
            * a one-hot-encoding array representing the index of a category: [0, 1, 0]

        Examples:
            categories => ["foo", "bar"]

            convert_to_expected_format(0) == 0
            convert_to_expected_format(3) == ValueError           # Out of range
            convert_to_expected_format("1") == 1
            convert_to_expected_format("5") == ValueError         # Out of range
            convert_to_expected_format("bar") == 1
            convert_to_expected_format("hue") == ValueError       # Not a valid category
            convert_to_expected_format([0]) == 0
            convert_to_expected_format([3]) == ValueError         # Out of range
            convert_to_expected_format([1, 0]) == 0
            convert_to_expected_format([0, 0, 1]) == ValueError   # Out of range

        Raises:
            ValueError: If the data can't be converted.
        """

        if isinstance(data, str):
            try:
                # "1"
                data_as_int = int(data)

            except ValueError:
                # "foo"
                data_as_int = self.categories.index(data)

        elif isinstance(data, int):
            # 1
            data_as_int = data

        elif isinstance(data, (list, tuple, np.ndarray)):
            if len(data) == 1:
                # [1]
                data_as_int = data[0]
            else:
                # [0, 1]
                data_as_int = np.argmax(data)
        else:
            raise ValueError

        if 0 <= data_as_int < len(self.categories):
            return data_as_int

        raise ValueError

    def __getstate__(self) -> dict:
        dc = super().__getstate__()
        dc["categories"] = self.categories

        return dc

    def __setstate__(self, new_state: dict):
        super().__setstate__(new_state)

        self.categories = new_state["categories"]

    def __reduce__(self):
        return (Categorical, (self.categories,), self.__getstate__())


DataTypeContainer.Categorical = providers.Factory(Categorical)
