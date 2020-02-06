# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import numpy as np

from .datatype import DataType


class ImageArray(DataType):
    """
    Image, represented as an array of int values, each one representing a pixel
    intensity (0-255).

    The array will have shape (W, H), for grayscale images, or (W, H, C), where C
    represents the number of color channels (For RGB images)
    """

    def process(self, data: np.ndarray) -> np.ndarray:
        return data.flatten()

    def display(self, data: np.ndarray):
        return data
