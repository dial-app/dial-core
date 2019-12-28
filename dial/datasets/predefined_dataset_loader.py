# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Classes for loading predefined datasets.
"""

from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from dial.datasets import Dataset, datatype
from tensorflow.keras.datasets import (boston_housing, cifar10, fashion_mnist,
                                       mnist)


class PredefinedDatasetLoader(metaclass=ABCMeta):
    """
    Abstract class for any predefined dataset.
    """

    def __init__(
        self, name="", brief="", x_type=datatype.Numeric(), y_type=datatype.Numeric()
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


class MnistLoader(PredefinedDatasetLoader):
    """
    Mnist dataset loader.
    """

    def __init__(self):
        super().__init__(
            "MNIST",
            "Handwritten digit numbers",
            datatype.ImageArray(),
            datatype.Numeric(),
        )

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = MnistLoader()

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset


class FashionMnistLoader(PredefinedDatasetLoader):
    """
    Fashion Mnist dataset loader.
    """

    def __init__(self):
        super().__init__(
            "Fashion-MNIST",
            "Categorized set of clothing images",
            datatype.ImageArray(),
            datatype.Categorical(),
        )

        self.y_type.categories = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = FashionMnistLoader()

        (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset

    @property
    def categories(self) -> List[str]:
        """
        Return the list of classes identified by Fashion-MNIST
        """
        return self.y_type.categories


class Cifar10Loader(PredefinedDatasetLoader):
    """
    Cifar10 dataset loader.
    """

    def __init__(self):
        super().__init__(
            "CIFAR10",
            "Categorized images.",
            datatype.ImageArray(),
            datatype.Categorical(),
        )

        self.y_type.categories = [
            "airplane",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = Cifar10Loader()

        (x_train, y_train), (x_test, y_test) = cifar10.load_data()

        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset

    @property
    def categories(self) -> List[str]:
        """
        Return the list of classes identified by CIFAR10
        """
        return self.y_type.categories


class BostonHousingLoader(PredefinedDatasetLoader):
    """
    Boston Housing dataset loader.
    """

    def __init__(self):
        super().__init__(
            "Boston Housing",
            "Boston House prices.",
            datatype.NumericArray(),
            datatype.Numeric(),
        )

    @staticmethod
    def load() -> Tuple[Dataset, Dataset]:
        dataset = BostonHousingLoader()

        (x_train, y_train), (x_test, y_test) = boston_housing.load_data()

        train_dataset = Dataset(x_train, y_train, dataset.x_type, dataset.y_type)
        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)

        return train_dataset, test_dataset


PREDEFINED_DATASETS = {
    "mnist": MnistLoader(),
    "fashion-mnist": FashionMnistLoader(),
    "cifar10": Cifar10Loader(),
    "boston-housing": BostonHousingLoader(),
}
