# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np

from dial_core.datasets import DatasetLoader, PredefinedDatasetLoaders, datatype


def test_dataset_loader():
    class CustomLoader(DatasetLoader):
        def __init__(self):
            super().__init__(
                "CustomLoader",
                "Custom Loader class",
                datatype.Numeric(),
                datatype.Numeric(),
            )

        def _load_data(self):
            return (np.array([1]), np.array([2])), (np.array([3]), np.array([4]))

    custom_loader = CustomLoader()

    train_dataset, test_dataset = custom_loader.load()

    assert len(train_dataset) == 1
    assert len(test_dataset) == 1

    assert train_dataset.head(1) == ([1], [2])
    assert test_dataset.head(1) == ([3], [4])


def test_mnist_loader():
    mnist_loader = PredefinedDatasetLoaders.Mnist()

    assert isinstance(mnist_loader.x_type, datatype.ImageArray)
    assert isinstance(mnist_loader.y_type, datatype.Categorical)

    assert mnist_loader.y_type.categories == [str(i) for i in range(0, 10)]

    assert str(mnist_loader) == "MNIST"


def test_fashion_mnist_loader():
    fashion_mnist_loader = PredefinedDatasetLoaders.FashionMnist()

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
    cifar10_loader = PredefinedDatasetLoaders.Cifar10()

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
    boston_housing_loader = PredefinedDatasetLoaders.BostonHousing()

    assert isinstance(boston_housing_loader.x_type, datatype.NumericArray)
    assert isinstance(boston_housing_loader.y_type, datatype.Numeric)

    assert str(boston_housing_loader) == "Boston Housing"
