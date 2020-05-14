# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Callable, List

import dependency_injector.providers as providers
import numpy as np

from .datatype import DataType, DataTypeContainer


class ImageArray(DataType):
    """
    The ImageArray class represents an image as amultidimensional array, each one with a
    pixel intensity.

    Pixels are stored on memory with values between (0-255), but they're transformed to
    the range (0-1) after the `process` method.

    The array will have shape (W, H) for grayscale images, or (W, H, C), where C
    represents the number of color channels (For RGB images it would be 3, for example)
    """

    def __init__(self):
        super().__init__()

        self.transformations: List[Callable] = []

    def process(self, data: "np.ndarray") -> "np.ndarray":
        """Returns `data` with pixel values in the range (0-1)."""
        data = data / 255.0

        if len(data.shape) == 2:
            data = np.expand_dims(data, axis=2)

        return self._apply_transformations(data)

    def display(self, data: "np.ndarray") -> "np.ndarray":
        """Returns the data _as it is_, and can be used to paint the image."""
        return data

    def convert_to_expected_format(self, data: "np.ndarray") -> "np.ndarray":
        """This class actually expects data to be passed correctly, as it is hard to
        translate from one format to another.
        """
        return np.array(data)

    def __reduce__(self):
        return (ImageArray, (), super().__getstate__())


DataTypeContainer.ImageArray = providers.Factory(ImageArray)
