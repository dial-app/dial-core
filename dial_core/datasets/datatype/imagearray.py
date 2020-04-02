# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from .datatype import DataType

if TYPE_CHECKING:
    import numpy as np


class ImageArray(DataType):
    """
    Image, represented as an array of int values, each one representing a pixel
    intensity (0-255).

    The array will have shape (W, H), for grayscale images, or (W, H, C), where C
    represents the number of color channels (For RGB images)
    """

    def process(self, data: "np.ndarray") -> "np.ndarray":
        data = data.flatten()
        data = data / 255.0

        return data

    def display(self, data: "np.ndarray"):
        return data

    def convert_to_expected_format(self, data) -> "np.array":
        return data
