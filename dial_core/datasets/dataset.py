# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING, Any, List, Tuple

import numpy as np
from tensorflow import keras

from .datatype import Numeric

if TYPE_CHECKING:
    from .datatype import DataType


class Dataset(keras.utils.Sequence):
    """The Dataset class is a data container. It can be used as a data generator by
    keras methos like fit, predict... and any other method that requires to be feed with
    data batches.

    Two Datatypes must also be provided. This classes specify how an specific data is
    stored on memory and how it should be loaded, processed, and returned.

    Attributes:
        x: x (input) array.
        y: y (output) array.
        x_type: Datatype of x array.
        y_type: Datatype of y array.
        batch_size: Batch size.
    """

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
        # Data arrays
        self.x = np.empty(0) if x_data is None else x_data
        self.y = np.empty(0) if y_data is None else y_data

        # Data types
        self.x_type = Numeric() if x_type is None else x_type
        self.y_type = Numeric() if y_type is None else y_type

        self.batch_size = batch_size

    @property
    def input_shape(self):
        """Returns the shape of the `_x` array, or (0,) if not loaded/not defined."""
        return self.x_type.process(self.x[0]).shape if len(self.x) > 0 else (0,)

    @property
    def output_shape(self):
        """Returns the shape of the `y` array, or (0,) if not loaded/not defined."""
        return self.y_type.process(self.y[0]).shape if len(self.y) else (0,)

    def insert(self, position: int, x: List[Any], y: List[Any]):
        """Inserts x and y elements at the given position.

        Raises:
            ValueError: If the two lists don't have the same length.
        """
        if len(x) != len(y):
            raise ValueError(f"Can't insert {len(x)} values on x and {len(y)} on y!")

        self.x = np.insert(self.x, position, x, axis=0)
        self.y = np.insert(self.y, position, y, axis=0)

    def delete_rows(self, start: int, n: int = 1):
        """Deletes `n` rows at `start` position, including `start`"""
        self.x = np.delete(self.x, range(start, start + n), axis=0)
        self.y = np.delete(self.y, range(start, start + n), axis=0)

    def head(self, n: int = 10, role: "Role" = Role.Raw) -> Tuple[List, List]:
        """Returns the first `n` items on the dataset."""
        return self.items(0, n, role)

    def items(
        self, start: int = None, end: int = None, role: "Role" = Role.Raw
    ) -> Tuple["np.array", "np.array"]:
        """Returns the `n` elements between start and end as a tuple of (x, y) items
        Range is EXCLUSIVE [start, end).
        """
        x_set, y_set = self._preprocess_data(self.x[start:end], self.y[start:end], role)
        return x_set, y_set

    def row_count(self) -> int:
        """Returns the number of rows on the dataset."""
        return len(self.x)

    def __len__(self) -> int:
        """Returns the length of the dataset (in batches)."""
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx: int) -> Tuple["np.array", "np.array"]:
        """Returns the batch of items starting at `idx`."""
        batch_start = idx * self.batch_size
        batch_end = (idx + 1) * self.batch_size

        batch_x = self.x[batch_start:batch_end]
        batch_y = self.y[batch_start:batch_end]

        batch_x, batch_y = self._preprocess_data(
            self.x[batch_start:batch_end], self.y[batch_start:batch_end]
        )

        return batch_x, batch_y

    def _preprocess_data(
        self, x_data: "np.array", y_data: "np.array", role: "Role" = Role.Raw
    ) -> Tuple["np.array", "np.array"]:
        """ Preprocess the data. For example, if the image is a path to a file, load it
        and return the corresponding array.
        """
        if role == self.Role.Raw:
            x_data = np.array([self.x_type.process(element) for element in x_data])
            y_data = np.array([self.y_type.process(element) for element in y_data])
        elif role == self.Role.Display:
            x_data = np.array([self.x_type.display(element) for element in x_data])
            y_data = np.array([self.y_type.display(element) for element in y_data])

        return (x_data, y_data)

    def __str__(self):
        return f"Dataset (x={self.x_type}, y={self.y_type})"
