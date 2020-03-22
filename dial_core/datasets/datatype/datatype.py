# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from abc import ABCMeta, abstractmethod


class DataType(metaclass=ABCMeta):
    """
    Abstract class for any data type.
    """

    def __init__(self):
        self.is_editable = False

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

    @abstractmethod
    def convert_to_expected_format(self, data):
        """
        Transforms the passed data to a format expected by the dataset, that can be
        stored.

        See the derived DataType classes (Categorical, Numeric...) for more
            explanations.

        Raises:
            ValueError: If the data can't be converted
        """
