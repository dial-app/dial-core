# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from abc import ABC, abstractmethod
from typing import List, Tuple

from keras.datasets import boston_housing, cifar10, fashion_mnist, mnist

from tfg.datasets import Dataset, DataType


class PredefinedDatasetLoader(ABC):
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


class MnistLoader(PredefinedDatasetLoader):
    """
    Mnist dataset loader.
    """

    def __init__(self):
        super().__init__(
            "MNIST", "Handwritten digit numbers", DataType.ImageArray, DataType.Numeric
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
            DataType.ImageArray,
            DataType.Categorical,
        )

        self.__categories = [
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
        train_dataset.y_categories = dataset.categories

        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)
        test_dataset.y_categories = dataset.categories

        return train_dataset, test_dataset

    @property
    def categories(self) -> List[str]:
        """
        Return the list of classes identified by Fashion-MNIST
        """
        return self.__categories


class Cifar10Loader(PredefinedDatasetLoader):
    """
    Cifar10 dataset loader.
    """

    def __init__(self):
        super().__init__(
            "CIFAR10", "Categorized images.", DataType.ImageArray, DataType.Categorical
        )

        self.__categories = [
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
        train_dataset.y_categories = dataset.categories

        test_dataset = Dataset(x_test, y_test, dataset.x_type, dataset.y_type)
        test_dataset.y_categories = dataset.categories

        return train_dataset, test_dataset

    @property
    def categories(self) -> List[str]:
        """
        Return the list of classes identified by CIFAR10
        """
        return self.__categories


class BostonHousingLoader(PredefinedDatasetLoader):
    """
    Boston Housing dataset loader.
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
