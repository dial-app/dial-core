# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtWidgets import QHeaderView, QTableView


class ModelTableView(QTableView):
    """
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
