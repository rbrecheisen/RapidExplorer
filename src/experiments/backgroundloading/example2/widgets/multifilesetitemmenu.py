from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView

from widgets.multifilesetitem import MultiFileSetItem


class MultiFileSetItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, multiFileSetItem: MultiFileSetItem, position: QPoint, parent=None) -> None:
        super(MultiFileSetItemMenu, self).__init__(parent)
        self._treeView = treeView
        self._item = multiFileSetItem
        self._position = position
        if not self._item.loaded():
            action1 = self.addAction('Load')
            action1.triggered.connect(self._handleLoadAction)
        action2 = self.addAction('Rename')
        action2.triggered.connect(self._handleRenameAction)
        action3 = self.addAction('Show in Main View')
        action3.triggered.connect(self._handleShowInMainViewAction)
        action4 = self.addAction('Delete')
        action4.triggered.connect(self._handleDeleteAction)

    def _handleLoadAction(self):
        pass

    def _handleRenameAction(self):
        pass

    def _handleShowInMainViewAction(self):
        pass

    def _handleDeleteAction(self):
        pass

    def show(self):
        self.exec_(self._position)