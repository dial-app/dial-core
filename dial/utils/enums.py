from enum import IntEnum

from PySide2.QtCore import Qt


class Dial(IntEnum):
    RawRole = Qt.UserRole  # The data in a raw format (as it is)
    TypeRole = Qt.UserRole + 1  # The type of the data (used with datatype.DataType)
