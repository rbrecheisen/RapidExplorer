from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView, QMessageBox

from widgets.filesetitem import FileSetItem
from plugins.pluginmanager import PluginManager
from plugins.viewplugin import ViewPlugin


class FileSetItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, fileSetItem: FileSetItem, position: QPoint) -> None:
        super(FileSetItemMenu, self).__init__()
        self._treeView = treeView
        self._fileSetItem = fileSetItem
        self._position = position
        self._pluginManager = PluginManager()
        action1 = self.addAction('Rename')
        action2 = self.addAction('Show in Main View')
        action1.triggered.connect(self._handleRenameAction)
        action2.triggered.connect(self._handleShowInMainViewAction)

    def _handleRenameAction(self):
        self._fileSetItem.setEditable(True)
        self._treeView.edit(self._treeView.model().indexFromItem(self._fileSetItem))
        self._fileSetItem.setEditable(False)

    def _handleShowInMainViewAction(self):
        currentPlugin = self._pluginManager.currentPlugin()
        if currentPlugin:
            if isinstance(currentPlugin, ViewPlugin):
                data = self._fileSetItem.registeredFileSetModel()
                currentPlugin.setData(data)
                return
        QMessageBox.critical(self, 'Error', 'No view plugin selected')

    def show(self):
        self.exec_(self._position)