# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QListView


class ModelsListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
