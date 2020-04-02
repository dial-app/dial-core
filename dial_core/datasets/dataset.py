# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING, Any, List, Tuple

import numpy as np
from tensorflow import keras

from .datatype import Numeric

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
    ):

        if x_data is None:
            x_data = np.empty(0)

        if y_data is None:
            y_data = np.empty(0)

        if x_type is None:
            x_type = Numeric()

        if y_type is None:
            y_type = Numeric()

        # Data arrays
        self.__x, self.__y = x_data, y_data

        # Data types
        self.x_type, self.y_type = x_type, y_type

        self.batch_size = batch_size

    @property
    def input_shape(self):
        return self.x_type.process(self.__x[0]).shape if len(self.__x) > 0 else (0,)

    def insert(self, position: int, x: List[Any], y: List[Any]):
        if len(x) != len(y):
            raise ValueError(f"Can't insert {len(x)} values on x and {len(y)} on y!")

        self.__x = np.insert(self.__x, position, x, axis=0)
        self.__y = np.insert(self.__y, position, y, axis=0)

    def delete_rows(self, start: int, n: int = 1):
        self.__x = np.delete(self.__x, range(start, start + n), axis=0)
        self.__y = np.delete(self.__y, range(start, start + n), axis=0)

    def head(self, n: int = 10, role: "Role" = Role.Raw) -> Tuple[List, List]:
        """
        Returns the first `n` items on the dataset.
        """
        return self.items(0, n, role)

    def items(
        self, start: int = None, end: int = None, role: "Role" = Role.Raw
    ) -> Tuple["np.array", "np.array"]:
        """
        Return the `n` elements between start and end as a tuple of (x, y) items
        Range is EXCLUSIVE [start, end)
        """
        x_set, y_set = self.__preprocess_data(
            self.__x[start:end], self.__y[start:end], role
        )
        return x_set, y_set

    def row_count(self) -> int:
        """Returns the number of rows on the dataset."""
        return len(self.__x)

    def __len__(self) -> int:
        """
        Return the length of the dataset (In batches)
        """
        return int(np.ceil(len(self.__x) / float(self.batch_size)))

    def __getitem__(self, idx: int) -> Tuple["np.array", "np.array"]:
        """
        Return the batch of items starting on `idx`.
        """
        batch_start = idx * self.batch_size
        batch_end = (idx + 1) * self.batch_size

        batch_x = self.__x[batch_start:batch_end]
        batch_y = self.__y[batch_start:batch_end]

        batch_x, batch_y = self.__preprocess_data(
            self.__x[batch_start:batch_end], self.__y[batch_start:batch_end]
        )

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
