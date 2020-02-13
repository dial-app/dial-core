# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtGui import QColor

from dial.datasets import Dataset


class TypeColor:
    colors = {
        int: QColor("#B54747"),
        str: QColor("#0056A6"),
        Dataset: QColor("#6666FF"),
    }

    @classmethod
    def get_color_for(cls, port_type):
        try:
            return cls.colors[port_type]
        except KeyError:
            return QColor("#000000")
