# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from abc import ABC, abstractmethod
from typing import Tuple

from keras.datasets import boston_housing, cifar10, mnist

from tfg.datasets import Dataset, DataType


class PredefinedDataset(ABC):
    """
    Abstract class for any predefined dataset.
    """

    def __init__(
        self, name="", brief="", x_type=DataType.Numeric, y_type=DataType.Numeric
    ):
        self.name = name
        self.brief = brief
        self.x_type = x_type
        self.y_type = y_type

    @staticmethod
    @abstractmethod
    def load() -> Tuple[Dataset, Dataset]:
        """
        Return the train/test dataset objects.
        """

    def __str__(self) -> str:
        return self.name


class MnistDataset(PredefinedDataset):
    """
    Mnist dataset.
    """

    def __init__(self):
        super().__init__(
            "MNIST", "Handwritten digit numbers", DataType.ImageArray, DataType.Numeric
        )

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = MnistDataset()

        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset


class Cifar10Dataset(PredefinedDataset):
    """
    Cifar10.
    """

    def __init__(self):
        super().__init__(
            "CIFAR10", "Categorized images.", DataType.ImageArray, DataType.Numeric
        )

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = Cifar10Dataset()

        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset


class BostonHousingDataset(PredefinedDataset):
    """
    Boston Housing Datasets.
    """

    def __init__(self):
        super().__init__(
            "Boston Housing",
            "Boston House prices.",
            DataType.NumericArray,
            DataType.Numeric,
        )

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = BostonHousingDataset()

        (x_train, y_train), (x_test, y_test) = boston_housing.load_data()
        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset
