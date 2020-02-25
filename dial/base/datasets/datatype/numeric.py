# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .datatype import DataType


class Numeric(DataType):
    """
    Represents a single numeric value.
    """

    def process(self, data: int) -> int:
        return data

    def display(self, data: int) -> str:
        return str(data)
