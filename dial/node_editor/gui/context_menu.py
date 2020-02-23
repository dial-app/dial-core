# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QMenu

from dial.gui.widgets.menus import FileMenu, NodesMenu
from dial.node_editor import NodeFactorySingleton

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class DialContextMenu(QMenu):
    def __init__(self, parent: "QWidget" = None):
        super().__init__("Menu", parent)

        self.addMenu(FileMenu(parent=self))
        self.addMenu(NodesMenu(node_factory=NodeFactorySingleton()))
