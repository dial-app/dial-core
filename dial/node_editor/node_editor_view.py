# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from PySide2.QtWidgets import QGraphicsView


class NodeEditorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()
