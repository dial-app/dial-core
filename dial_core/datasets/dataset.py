# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING, List, Tuple

import numpy as np
from tensorflow import keras

from .datatype import NumericArray

if TYPE_CHECKING:
    from .datatype import DataType


class Dataset(keras.utils.Sequence):
    class Role(Enum):
        Raw = 0
        Display = 1

    def __init__(
        self,
        x_data: "np.ndarray" = None,
        y_data: "np.ndarray" = None,
        x_type: "DataType" = None,
        y_type: "DataType" = None,
        batch_size: int = 32,
        shuffled: bool = False,
    ):

        if x_data is None:
            x_data = np.empty(0)

        if y_data is None:
            y_data = np.empty(0)

        if x_type is None:
            x_type = NumericArray()

        if y_type is None:
            y_type = NumericArray()

        # Data arrays
        self.__x, self.__y = x_data, y_data

        # Data types
        self.x_type, self.y_type = x_type, y_type

        # Class attributes
        self.__indexes = np.arange(self.__x.shape[0])

        self.shuffled = shuffled  # type: ignore

        self.batch_size = batch_size

    @property
    def shuffled(self) -> bool:
        """
        Check if the dataset is shuffled (dataset items randomly sorted)
        """
        return self.__shuffled

    @shuffled.setter  # type: ignore
    def shuffled(self, toggle: bool):
        self.__shuffled = toggle

        if self.__shuffled:
            self.shuffle()
        else:
            self.__indexes = np.arange(self.__x.shape[0])

    def shuffle(self):
        self.__shuffled = True
        np.random.shuffle(self.__indexes)

    def delete_rows(self, start: int, n: int = 1):
        self.__x = np.delete(self.__x, self.__indexes[start : start + n])
        self.__y = np.delete(self.__y, self.__indexes[start : start + n])
        self.__indexes = np.delete(self.__indexes, range(start, start + n - 1))

    def head(self, n: int = 10, role: "Role" = Role.Raw) -> Tuple[List, List]:
        """
        Returns the first `n` items on the dataset.
        """
        return self.items(0, n, role)

    def items(
        self, start: int, end: int, role: "Role" = Role.Raw
    ) -> Tuple["np.array", "np.array"]:
        """
        Return the `n` elements between start and end as a tuple of (x, y) items
        Range is EXCLUSIVE [start, end)
        """
        start = max(start, 0)
        end = min(end, len(self.__indexes))
        indexes = self.__indexes[start:end]

        x_set, y_set = self.__preprocess_data(
            self.__x[indexes], self.__y[indexes], role
        )
        return x_set, y_set

    def __len__(self) -> int:
        """
        Return the length of the dataset.
        """
        return int(np.ceil(len(self.__x) / float(self.batch_size)))

    def __getitem__(self, idx: int) -> Tuple["np.array", "np.array"]:
        """
        Return the batch of items starting on `idx`.
        """
        batch_start = idx * self.batch_size
        batch_end = (idx + 1) * self.batch_size
        batch_indexes = self.__indexes[batch_start:batch_end]

        batch_x = self.__x[batch_indexes]
        batch_y = self.__y[batch_indexes]

        batch_x, batch_y = self.__preprocess_data(batch_x, batch_y)

        return batch_x, batch_y

    def __preprocess_data(
        self, x_data: "np.array", y_data: "np.array", role: "Role" = Role.Raw
    ) -> Tuple["np.array", "np.array"]:
        """
        Preprocess the data. For example, if the image is a path to a file, load it and
        return the corresponding array.
        """
        if role == self.Role.Raw:
            x_data = np.array([self.x_type.process(element) for element in x_data])
            y_data = np.array([self.y_type.process(element) for element in y_data])
        elif role == self.Role.Display:
            x_data = np.array([self.x_type.display(element) for element in x_data])
            y_data = np.array([self.y_type.display(element) for element in y_data])

        return (x_data, y_data)
