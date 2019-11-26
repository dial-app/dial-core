# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QListView


class PredefinedDatasetsListView(QListView):
    def __init__(self, parent):
        super().__init__(parent)
