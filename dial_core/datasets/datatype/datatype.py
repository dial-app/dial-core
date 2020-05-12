# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from abc import ABCMeta, abstractmethod
from typing import Any, Callable, List

import dependency_injector.containers as containers


class DataType(metaclass=ABCMeta):
    """
    Abstract class for any data type.

    Subclass this class for defining new types that Dataset objects can store.

    This class must provide an implementation for `process` and `display` methods. See
    the methods documentation for more information.
    """

    def __init__(self):
        self.is_editable = False

        self.transformations: List[Callable] = []

    @abstractmethod
    def process(self, data):
        """Returns the data after processing given the data type.

        For example, if the DataType is an ImagePath, process() will open the image and
        return the array corresponding to its content.
        """

    @abstractmethod
    def display(self, data):
        """Returns the display representation of the data.

        For example, for Categorical types this will be the actual category name instead
        of the interger.
        """

    @abstractmethod
    def convert_to_expected_format(self, data):
        """Transforms the passed data to a format expected to be stored by the dataset.

        See the derived DataType classes (Categorical, Numeric...) for more
        explanations.

        Raises:
            ValueError: If the data can't be converted
        """

    def to_dict(self):
        return self.__getstate__()

    def from_dict(self, dc: dict):
        self.__setstate__(dc)

        return self

    @classmethod
    def create(cls, dc: dict):
        if not dc:
            return None

        try:
            return getattr(DataTypeContainer, dc["class"])().from_dict(dc)

        except KeyError:
            return None

    def _apply_transformations(self, value: Any):
        result = value
        for f in self.transformations:
            result = f(result)

        return result

    def __getstate__(self) -> dict:
        return {"class": str(self)}

    def __setstate__(self, new_state: dict):
        pass

    def __reduce__(self):
        return (DataType, (), self.__getstate__())

    def __str__(self) -> str:
        return type(self).__name__


DataTypeContainer = containers.DynamicContainer()
