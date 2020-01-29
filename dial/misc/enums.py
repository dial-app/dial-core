# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum

from PySide2.QtCore import Qt


class Dial(Enum):
    TypeRole = Qt.UserRole + 1  # The type of the data (used with datatype.DataType)
    KerasLayerDictMIME = "application/layer"
