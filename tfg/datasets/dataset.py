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

from enum import Enum
from typing import List, Tuple

import keras
import numpy as np
from PIL import Image


class DataType(Enum):
    """
    Data Types that the dataset could use as Input/Output.
    """

    ImageArray = 1
    ImagePath = 2
    Numeric = 3
    NumericArray = 4

    def __str__(self):
        return self.name


class Dataset(keras.utils.Sequence):
    """
    Dataset generator
    """

    def __init__(
        self,
        x_data: List,
        y_data: List,
        x_type: DataType,
        y_type: DataType,
        batch_size: int = 32,
        shuffled: bool = False,
    ):
        self.__x, self.__y = x_data, y_data
        self.__x_type, self.__y_type = x_type, y_type

        self.__indexes = np.arange(self.__x.shape[0])

        self.shuffled = shuffled

        self.batch_size = batch_size

    @property
    def shuffled(self) -> bool:
        return self.__shuffled

    @shuffled.setter
    def shuffled(self, toggle: bool):
        self.__shuffled = toggle

        if self.__shuffled:
            np.random.shuffle(self.__indexes)
        else:
            self.__indexes = np.arange(self.__x.shape[0])

    @property
    def x_type(self) -> DataType:
        return self.__x_type

    @property
    def y_type(self) -> DataType:
        return self.__y_type

    def head(self, items: int = 10) -> Tuple[List, List]:
        """
        Returns the first `items` items on the dataset.
        """
        indexes = self.__indexes[:items]

        x_head, y_head = self.__preprocess_data(self.__x[indexes], self.__y[indexes])
        return x_head, y_head

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

        # TODO: Move Image "resize" to another place
        if self.__x_type is DataType.ImagePath:
            x_data = [Image.open(file_name).resize(200, 200) for file_name in x_data]
            # np.vectorize(lambda img: Image.open(img).resize(20, 20))(x_data)

        if self.__y_type is DataType.ImagePath:
            y_data = [Image.open(file_name).resize(200, 200) for file_name in y_data]

        return (x_data, y_data)
