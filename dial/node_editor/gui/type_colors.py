# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtGui import QColor
from tensorflow.keras import Model

from dial.datasets import Dataset
from dial.misc import Dial


class TypeColor:
    colors = {
        int: QColor("#B54747"),
        str: QColor("#0056A6"),
        Dataset: QColor("#6666FF"),
        Dial.KerasLayerListMIME: QColor("#AA0000"),
        Model: QColor("#0000AA"),
    }

    @classmethod
    def get_color_for(cls, port_type):
        try:
            return cls.colors[port_type]
        except KeyError:
            return QColor("#000000")
