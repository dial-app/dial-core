# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QListView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class DatasetsListView(QListView):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)
