from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu

from data.databasemanager import DatabaseManager
from data.registeredmultifilesetcontentloader import RegisteredMultiFileSetContentLoader
from widgets.multifilesetitem import MultiFileSetItem


class MultiFileSetItemMenu(QMenu):
    def __init__(self, treeView, multiFileSetItem: MultiFileSetItem, position: QPoint, parent=None) -> None:
        super(MultiFileSetItemMenu, self).__init__(parent)
        self._treeView = treeView
        self._multiFileSetItem = multiFileSetItem
        self._position = position
        self._databaseManager = DatabaseManager()
        if not self._multiFileSetItem.loaded():
            action1 = self.addAction('Load')
            action1.triggered.connect(self._handleLoadAction)
        action2 = self.addAction('Rename')
        action2.triggered.connect(self._handleRenameAction)
        action3 = self.addAction('Show in Main View')
        action3.triggered.connect(self._handleShowInMainViewAction)
        action4 = self.addAction('Delete')
        action4.triggered.connect(self._handleDeleteAction)

    def _handleLoadAction(self):
        self._treeView.progressDialog().show()
        self._treeView.progressDialog().setValue(0)
        registeredMultiFileSetModel = self._multiFileSetItem.registeredMultiFileSetModel()
        loader = RegisteredMultiFileSetContentLoader(registeredMultiFileSetModel)
        loader.signal().progress.connect(self._contentLoaderProgress)
        loader.execute()

    def _handleRenameAction(self):
        self._multiFileSetItem.setEditable(True)
        self._treeView.edit(self._treeView.model().indexFromItem(self._multiFileSetItem))
        self._multiFileSetItem.setEditable(False)

    def _handleShowInMainViewAction(self):
        pass

    def _handleDeleteAction(self):
        registeredMultiFileSetModel = self._multiFileSetItem.registeredMultiFileSetModel()
        self._databaseManager.deleteData(registeredMultiFileSetModel)
        # cache = FileCache()
        # cache.removeMultiFileSet(registeredMultiFileSetModel)
        # with DbSession() as session:
        #     model = session.get(MultiFileSetModel, registeredMultiFileSetModel.id)
        #     session.delete(model)
        #     session.commit()
        self._treeView.model().clear()
        self._treeView.loadModelsFromDatabase()
    
    def _contentLoaderProgress(self, progress):
        self._treeView.progressDialog().setValue(progress)
        if progress == 100:
            self._treeView.model().clear()
            self._treeView.loadModelsFromDatabase()

    def show(self):
        self.exec_(self._position)