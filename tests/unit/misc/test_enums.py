# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from PySide2.QtCore import Qt

from dial.misc import Dial


@pytest.mark.parametrize(
    "enum, value",
    [
        (Dial.TypeRole, Qt.UserRole),
        (Dial.KerasLayerListMIME, "application/keras.layer.list"),
    ],
)
def test_enum_values(enum, value):
    assert enum.value == value
