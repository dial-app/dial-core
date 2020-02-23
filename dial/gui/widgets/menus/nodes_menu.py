# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial.node_editor import NodeFactory


class NodesMenu(QMenu):
    def __init__(self, node_factory: "NodeFactory", parent: "QWidget" = None):
        super().__init__("&Nodes", parent)

        for node_name, node in node_factory.nodes:
            action = QAction(node_name, self)
            self.addAction(action)
