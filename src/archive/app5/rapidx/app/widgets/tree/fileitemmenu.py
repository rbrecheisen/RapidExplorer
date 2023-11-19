from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from rapidx.app.widgets.tree.fileitem import FileItem
from rapidx.app.plugins.pluginmanager import PluginManager


class FileItemMenu(QMenu):
    def __init__(self, treeView, item: FileItem, position: QPoint, parent=None) -> None:
        super(FileItemMenu, self).__init__(parent)
        self._treeView = treeView
        self._item = item
        self._position = position
        showInMainViewAction = self.addAction('Show in Main View')
        showInMainViewAction.triggered.connect(self._handleShowInMainViewAction)

    def _handleShowInMainViewAction(self):
        manager = PluginManager()
        plugin = manager.currentPlugin()
        if plugin.supportsMethod('setFileModel'):
            plugin.setFileModel(self._item.fileModel())
            
    def show(self):
        self.exec_(self._position)