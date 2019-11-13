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
from keras.datasets import mnist
from skimage.io import imread
from skimage.transform import resize


class DataType(Enum):
    IMAGE_ARRAY = 1
    IMAGE_PATH = 2
    NUMERIC = 3


class DataArray:
    def __init__(self, data, data_type):
        self.data = data
        self.data_type = data_type

    def __getitem__(self, idx):
        return self.data[idx]


class Dataset(keras.utils.Sequence):
    """
    Dataset generator
    """

    def __init__(self, x_set, y_set, batch_size=32):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.x) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.x[idx * self.batch_size : (idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size : (idx + 1) * self.batch_size]

        if self.x.data_type is DataType.IMAGE_PATH:
            batch_x = [resize(imread(file_name), (200, 200)) for file_name in batch_x]

        return np.array(batch_x), np.array(batch_y)


if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train_array = DataArray(x_train, DataType.IMAGE_ARRAY)
    y_train_array = DataArray(y_train, DataType.NUMERIC)

    dset = Dataset(x_train_array, y_train_array)

    print("Dataset loaded")

    bx, by = dset[0]

    plt.imshow(bx[1])
    plt.show()
