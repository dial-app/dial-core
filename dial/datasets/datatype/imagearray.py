# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets.datatype import DataType
from typing import List


class ImageArray(DataType):
    """
    Image, represented as an array of int values, each one representing a pixel
    intensity (0-255).

    The array will have shape (W, H), for grayscale images, or (W, H, C), where C
    represents the number of color channels (For RGB images)
    """

    def process(self, data: List[int]) -> List[int]:
        return data

    def display(self, data: List[int]) -> str:
        return str(data)
