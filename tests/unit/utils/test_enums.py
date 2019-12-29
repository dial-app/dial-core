# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from dial.utils import Dial
from PySide2.QtCore import Qt


@pytest.mark.parametrize(
    "enum, value", [(Dial.RawRole, Qt.UserRole), (Dial.TypeRole, Qt.UserRole + 1)]
)
def test_enum_values(enum, value):
    assert enum == value
