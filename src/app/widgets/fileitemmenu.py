from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from widgets.fileitem import FileItem


class FileItemMenu(QMenu):
    def __init__(self, fileItem: FileItem, position: QPoint) -> None:
        super(FileItemMenu, self).__init__()
        self._item = fileItem
        self._position = position
        action1 = self.addAction('Show in Main View')
        action1.triggered.connect(self._handleShowInMainViewAction)

    def _handleShowInMainViewAction(self):
        pass

    def show(self):
        self.exec_(self._position)