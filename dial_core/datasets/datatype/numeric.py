# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any

from .datatype import DataType


class Numeric(DataType):
    """
    Represents a single numeric value.
    """

    def __init__(self):
        self.is_editable = True

    def process(self, data: int) -> int:
        return data

    def display(self, data: int) -> str:
        return str(data)

    def convert_to_expected_format(self, data: Any) -> int:
        return int(data)
