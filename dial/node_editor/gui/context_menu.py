# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QMenu

from dial.gui.widgets.menus import FileMenu, NodesMenu
from dial.node_editor import NodeFactorySingleton

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial.node_editor.gui import GraphicsScene, NodeEditorView


class DialContextMenu(QMenu):
    def __init__(
        self,
        graphics_scene: "GraphicsScene",
        node_editor_view: "NodeEditorView",
        parent: "QWidget" = None,
    ):
        super().__init__("Menu", parent)

        self.addMenu(FileMenu(parent=self))
        self.addMenu(
            NodesMenu(
                node_factory=NodeFactorySingleton(),
                graphics_scene=graphics_scene,
                node_editor_view=node_editor_view,
            )
        )
