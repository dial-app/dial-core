# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from keras.datasets import boston_housing, cifar10, mnist

from . import Dataset, DataType


def mnist_loader():
    (x_train, y_train), _ = mnist.load_data()
    train_dataset = Dataset(x_train, y_train, DataType.IMAGE_ARRAY, DataType.NUMERIC)

    return train_dataset


def cifar10_loader():
    (x_train, y_train), _ = cifar10.load_data()
    train_dataset = Dataset(x_train, y_train, DataType.IMAGE_ARRAY, DataType.NUMERIC)

    return train_dataset


def boston_housing_price_loader():
    (x_train, y_train), _ = boston_housing.load_data()
    train_dataset = Dataset(x_train, y_train, DataType.IMAGE_ARRAY, DataType.NUMERIC)

    return train_dataset
