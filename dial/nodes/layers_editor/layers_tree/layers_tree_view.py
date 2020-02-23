# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QAbstractItemView, QTreeView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class LayersTreeView(QTreeView):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.setDragEnabled(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
