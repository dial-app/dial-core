# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from abc import ABCMeta, abstractmethod
from typing import Tuple

import numpy as np
from tensorflow.keras.datasets import boston_housing, cifar10, fashion_mnist, mnist

from dial_core.datasets import Dataset, TTVSets, datatype
from dial_core.utils import Timer, log

LOGGER = log.get_logger(__name__)


class TTVSetsLoader(metaclass=ABCMeta):
    """The TTVSetsLoader class provides an abstract interface for defining classes that
    can load predefined TTVSets, like the ones included with keras.
    """

    def __init__(
        self,
        name: str,
        brief: str,
        x_type: "datatype.DataType",
        y_type: "datatype.DataType",
    ):
        self.name = name
        self.brief = brief
        self.x_type = x_type
        self.y_type = y_type

    def load(self) -> "TTVSets":
        """
        Load and return the train/test dataset objects.
        """
        with Timer() as timer:
            train, test, validation = self._load_data()

        LOGGER.info("Fetched dataset data in %s ms", timer.elapsed())

        return TTVSets(name=self.name, train=train, test=test, validation=validation)

    @abstractmethod
    def _load_data(self) -> Tuple["Dataset", "Dataset", "Dataset"]:  # pragma: no cover
        """
        Returns the TTVSets instance.
        """

    def __str__(self) -> str:
        return self.name


class MnistLoader(TTVSetsLoader):
    """Mnist dataset loader."""

    def __init__(self):
        super().__init__(
            "MNIST",
            "Handwritten digit numbers",
            datatype.ImageArray(),
            datatype.Categorical([str(i) for i in range(0, 10)]),
        )

    def _load_data(self):  # pragma: no cover
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        train = Dataset(x_train, y_train, self.x_type, self.y_type)
        test = Dataset(x_test, y_test, self.x_type, self.y_type)

        return train, test, None


class FashionMnistLoader(TTVSetsLoader):
    """Fashion Mnist dataset loader."""

    y_type: datatype.Categorical

    def __init__(self):
        super().__init__(
            "Fashion MNIST",
            "Categorized set of clothing images",
            datatype.ImageArray(),
            datatype.Categorical(
                [
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
            ),
        )

    def _load_data(self):  # pragma: no cover
        (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

        train = Dataset(x_train, y_train, self.x_type, self.y_type)
        test = Dataset(x_test, y_test, self.x_type, self.y_type)

        return train, test, None


class Cifar10Loader(TTVSetsLoader):
    """Cifar10 dataset loader."""

    y_type: datatype.Categorical

    def __init__(self):
        super().__init__(
            "CIFAR10",
            "Categorized images.",
            datatype.ImageArray(),
            datatype.Categorical(
                [
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
            ),
        )

    def _load_data(self):  # pragma: no cover
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()

        train = Dataset(x_train, y_train, self.x_type, self.y_type)
        test = Dataset(x_test, y_test, self.x_type, self.y_type)

        train.y = np.array(
            [train.y_type.convert_to_expected_format(i) for i in train.y]
        )
        test.y = np.array([test.y_type.convert_to_expected_format(i) for i in test.y])

        return train, test, None


class BostonHousingLoader(TTVSetsLoader):
    """Boston Housing dataset loader."""

    def __init__(self):
        super().__init__(
            "Boston Housing",
            "Boston House prices.",
            datatype.NumericArray(),
            datatype.Numeric(),
        )

    def _load_data(self):  # pragma: no cover
        (x_train, y_train), (x_test, y_test) = boston_housing.load_data()

        train = Dataset(x_train, y_train, self.x_type, self.y_type)
        test = Dataset(x_test, y_test, self.x_type, self.y_type)

        return train, test, None
