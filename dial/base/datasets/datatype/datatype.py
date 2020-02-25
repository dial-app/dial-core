# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from abc import ABCMeta, abstractmethod


class DataType(metaclass=ABCMeta):
    """
    Abstract class for any data type.
    """

    @abstractmethod
    def process(self, data):
        """
        Return the data after processing given the data type.

        For example, if the DataType is an ImagePath, process() will open the image and
        return the array corresponding to its content.
        """

    @abstractmethod
    def display(self, data):
        """
        Return the display representation of the data.

        For example, for Categorical types this will be the actual category name instead
        of an interger.
        """

    def __str__(self) -> str:
        return type(self).__name__
