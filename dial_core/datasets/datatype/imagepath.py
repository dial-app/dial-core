# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from typing import Callable, List

import dependency_injector.providers as providers
import numpy as np
from PIL import Image

from .datatype import DataType, DataTypeContainer


class ImagePath(DataType):
    """ The ImagePath class represents an image as an absolute path to a file that will
    be loading while training."""

    def __init__(self):
        super().__init__()

        self.transformations: List[Callable] = []

    def process(self, data: str) -> "np.ndarray":
        """Returns `data` as an array with pixel values in the range (0-1)."""
        image_array = self.display(data)

        image_array = image_array / 255.0

        return self._apply_transformations(image_array)

    def display(self, data: "np.ndarray") -> "np.ndarray":
        """Returns the loaded data _as it is_. Can be used to paint the image."""
        image = Image.open(data)
        image_array = np.array(image)

        return image_array

    def convert_to_expected_format(self, image: "str") -> "np.ndarray":
        """This class actually expects data to be passed correctly, as it is hard to
        translate from one format to another.
        """
        return os.path.abspath(image)

    def __reduce__(self):
        return (ImagePath, (), super().__getstate__())


DataTypeContainer.ImagePath = providers.Factory(ImagePath)
