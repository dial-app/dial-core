# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Various identifiers used throughout the Dial application."""


from enum import Enum

from PySide2.QtCore import Qt


class Dial(Enum):
    """The Dial class contains several identifiers used throughout the application."""
    TypeRole = Qt.UserRole
    KerasLayerListMIME = "application/keras.layer.list"
