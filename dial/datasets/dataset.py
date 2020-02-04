# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Notes:

Inputs:
    - From Keras (Predefined dataset): x_train, x_test, y_train, y_test
    - From local:
        * folders (train_folder, test_folder) with data inside (normally images) csv
        * csv files (train.csv, test.csv) with values inside csv files (train_csv,
            test_csv).
        * csv files (train.csv, test.csv). )The csv has a "path" to a resource, p.e:
            (./foo/1.jpg)
        * npy files (train.npy, test.npy) that can be loaded to numpy arrays

For a sequence of data (array), define the type of data using (categorical, numerical,
image...)
"""

from typing import List, Tuple

import numpy as np
from tensorflow import keras

from dial.datasets.datatype import DataType, NumericArray


class Dataset(keras.utils.Sequence):
    """
    Dataset generator
    """

    def __init__(
        self,
        x_data: np.ndarray = None,
        y_data: np.ndarray = None,
        x_type: DataType = None,
        y_type: DataType = None,
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

        self.shuffled = shuffled

        self.batch_size = batch_size

    @property
    def shuffled(self) -> bool:
        """
        Check if the dataset is shuffled (dataset items randomly sorted)
        """
        return self.__shuffled

    @shuffled.setter
    def shuffled(self, toggle: bool):
        self.__shuffled = toggle

        if self.__shuffled:
            self.shuffle()
        else:
            self.__indexes = np.arange(self.__x.shape[0])

    def shuffle(self):
        self.__shuffled = True
        np.random.shuffle(self.__indexes)

    def head(self, n_items: int = 10) -> Tuple[List, List]:
        """
        Returns the first `n` items on the dataset.
        """
        return self.items(0, n_items + 1)

    def items(self, start: int, end: int,) -> Tuple[List, List]:
        """
        Return the `n` elements between start and end as a tuple of (x, y) items
        Range is EXCLUSIVE [start, end)
        """
        indexes = self.__indexes[start:end]

        x_set, y_set = self.__preprocess_data(self.__x[indexes], self.__y[indexes])
        return x_set, y_set

    def __len__(self) -> int:
        """
        Return the length of the dataset.
        """
        return int(np.ceil(len(self.__x) / float(self.batch_size)))

    def __getitem__(self, idx) -> Tuple[List, List]:
        """
        Return the batch of dataset items starting on `idx`.
        """
        batch_indexes = self.__indexes[
            idx * self.batch_size : (idx + 1) * self.batch_size
        ]

        batch_x = self.__x[batch_indexes]
        batch_y = self.__y[batch_indexes]

        batch_x, batch_y = self.__preprocess_data(batch_x, batch_y)

        return np.array(batch_x), np.array(batch_y)

    def __preprocess_data(self, x_data: List, y_data: List) -> Tuple[List, List]:
        """
        Preprocess the data. For example, if the image is a path to a file, load it and
        return the corresponding array.
        """

        x_data = [self.x_type.process(element) for element in x_data]
        y_data = [self.y_type.process(element) for element in y_data]

        return (x_data, y_data)
