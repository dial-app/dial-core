# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QEvent, QRectF
from PySide2.QtWidgets import QGraphicsItem


class ResizableItemEventFilter(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem = None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemHasNoContents)

    def sceneEventFilter(self, item: QGraphicsItem, event: QEvent) -> bool:
        print(event)
        return super().sceneEventFilter(item, event)

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)
