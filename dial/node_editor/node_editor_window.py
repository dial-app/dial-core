# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QVBoxLayout, QWidget

from dial.node_editor import NodeEditorScene, NodeEditorView


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView()
        self.__node_editor_scene = NodeEditorScene()

        self.__node_editor_view.setScene(self.__node_editor_scene)

        self.__setup_ui()

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)
