# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial.node_editor import NodeFactory, Node
    from dial.node_editor.gui import GraphicsScene, NodeEditorView


class NodesMenu(QMenu):
    def __init__(
        self,
        node_factory: "NodeFactory",
        graphics_scene: "GraphicsScene",
        node_editor_view: "NodeEditorView",
        parent: "QWidget" = None,
    ):
        super().__init__("&Nodes", parent)

        self.__graphics_scene = graphics_scene
        self.__node_editor_view = node_editor_view

        for node_name, node_factory in node_factory.nodes.items():
            action = QAction(node_name, self)

            action.triggered.connect(
                lambda _=False, node_factory=node_factory: self.__add_node_to_scene(
                    node_factory()
                )
            )

            self.addAction(action)

    def __add_node_to_scene(self, node: "Node"):
        graphics_node = self.__graphics_scene.add_node_to_graphics(node)

        global_pos = self.__node_editor_view.mapFromGlobal(self.pos())
        graphics_node.setPos(self.__node_editor_view.mapToScene(global_pos))
