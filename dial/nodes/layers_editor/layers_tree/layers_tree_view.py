# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QAbstractItemView, QTreeView


class LayersTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
