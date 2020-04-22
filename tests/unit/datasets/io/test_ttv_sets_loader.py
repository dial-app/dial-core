# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np

from dial_core.datasets import Dataset, datatype
from dial_core.datasets.io import PredefinedTTVSetsContainer, TTVSetsLoader


def test_dataset_loader():
    class CustomLoader(TTVSetsLoader):
        def __init__(self):
            super().__init__(
                "CustomLoader",
                "Custom Loader class",
                datatype.NumericArray(),
                datatype.NumericArray(),
            )

        def _load_data(self):
            train = Dataset(np.array([1]), np.array([10]), self.x_type, self.y_type)
            test = Dataset(np.array([2]), np.array([20]), self.x_type, self.y_type)
            validation = Dataset(
                np.array([3]), np.array([30]), self.x_type, self.y_type
            )

            return train, test, validation

    custom_loader = CustomLoader()

    ttv = custom_loader.load()

    assert len(ttv.train) == 1
    assert len(ttv.test) == 1
    assert len(ttv.validation) == 1

    assert ttv.train.head(1) == ([1], [10])
    assert ttv.test.head(1) == ([2], [20])
    assert ttv.validation.head(1) == ([3], [30])


def test_mnist_loader():
    mnist_loader = PredefinedTTVSetsContainer.Mnist()

    assert isinstance(mnist_loader.x_type, datatype.ImageArray)
    assert isinstance(mnist_loader.y_type, datatype.Categorical)

    assert mnist_loader.y_type.categories == [str(i) for i in range(0, 10)]

    assert str(mnist_loader) == "MNIST"


def test_fashion_mnist_loader():
    fashion_mnist_loader = PredefinedTTVSetsContainer.FashionMnist()

    assert isinstance(fashion_mnist_loader.x_type, datatype.ImageArray)
    assert isinstance(fashion_mnist_loader.y_type, datatype.Categorical)

    assert fashion_mnist_loader.y_type.categories == [
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

    assert str(fashion_mnist_loader) == "Fashion MNIST"


def test_cifar10_loader():
    cifar10_loader = PredefinedTTVSetsContainer.Cifar10()

    assert isinstance(cifar10_loader.x_type, datatype.ImageArray)
    assert isinstance(cifar10_loader.y_type, datatype.Categorical)

    assert cifar10_loader.y_type.categories == [
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

    assert str(cifar10_loader) == "CIFAR10"


def test_boston_housing_loader():
    boston_housing_loader = PredefinedTTVSetsContainer.BostonHousing()

    assert isinstance(boston_housing_loader.x_type, datatype.NumericArray)
    assert isinstance(boston_housing_loader.y_type, datatype.Numeric)

    assert str(boston_housing_loader) == "Boston Housing"
