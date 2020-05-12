# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Callable, List

import dependency_injector.providers as providers

from .datatype import DataType, DataTypeContainer


class Numeric(DataType):
    """
    The Numeric class just represents a single interger.
    """

    def __init__(self):
        self.is_editable = True

        self.transformations: List[Callable] = []

    def process(self, data: int) -> int:
        """Returns the number. It doesn't need any processing."""
        return self._apply_transformations(data)

    def display(self, data: int) -> str:
        """Returns the interger as a string."""
        return str(data)

    def convert_to_expected_format(self, data: Any) -> int:
        """Transforms `data` to an interger.

        Raises:
            ValueError, TypeError: if data can't be transformed.
        """
        return int(data)

    def __reduce__(self):
        return (Numeric, (), super().__getstate__())


DataTypeContainer.Numeric = providers.Factory(Numeric)
