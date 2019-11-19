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

import keras
import matplotlib.pyplot as plt
import numpy as np
from keras.datasets import cifar10, mnist
from PIL import Image


class DataType(Enum):
    IMAGE_ARRAY = 1
    IMAGE_PATH = 2
    NUMERIC = 3


class Dataset(keras.utils.Sequence):
    """
    Dataset generator
    """

    def __init__(self, x_set, y_set, x_type, y_type, batch_size=32):
        self.x, self.y = x_set, y_set
        self.x_type, self.y_type = x_type, y_type
        self.batch_size = batch_size

    def head(self, items=10):
        x, y = self._preprocess_data(self.x[:items], self.y[:items])
        return zip(x, y)

    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size : (idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size : (idx + 1) * self.batch_size]

        batch_x, batch_y = self._preprocess_data(batch_x, batch_y)

        return np.array(batch_x), np.array(batch_y)

    def _preprocess_data(self, x, y):
        if self.x_type is DataType.IMAGE_PATH:
            x = [Image.open(file_name).resize(200, 200) for file_name in x]

        return (x, y)


if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    train_dataset = Dataset(x_train, y_train, DataType.IMAGE_ARRAY, DataType.NUMERIC)

    x, y = train_dataset[0]

    plt.imshow(x[0])
    plt.show()
