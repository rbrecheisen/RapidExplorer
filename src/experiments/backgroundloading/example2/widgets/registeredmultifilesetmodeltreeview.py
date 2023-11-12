from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItemModel, QMouseEvent

from data.dbsession import DbSession
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from widgets.multifilesetitem import MultiFileSetItem
from widgets.multifilesetitemmenu import MultiFileSetItemMenu
from widgets.filesetitem import FileSetItem
from widgets.filesetitemmenu import FileSetItemMenu
from widgets.fileitem import FileItem
from widgets.fileitemmenu import FileItemMenu


class RegisteredMultiFileSetModelTreeView(QTreeView):
    def __init__(self) -> None:
        super(RegisteredMultiFileSetModelTreeView, self).__init__()
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['Data'])
        self._model.itemChanged.connect(self._itemChanged)
        self.setModel(self._model)

    def addRegisteredMultiFileSetModel(self, registeredMultiFileSetModel: RegisteredMultiFileSetModel, loaded: bool=True) -> None:
        multiFileSetItem = MultiFileSetItem(registeredMultiFileSetModel, loaded)
        multiFileSetItem.setEditable(False)
        for registeredFileSetModel in registeredMultiFileSetModel.registeredFileSetModels:
            fileSetItem = FileSetItem(registeredFileSetModel)
            fileSetItem.setEditable(False)
            multiFileSetItem.appendRow(fileSetItem)
            for registeredFileModel in registeredFileSetModel.registeredFileModels:
                fileItem = FileItem(registeredFileModel)
                fileItem.setEditable(False)
                fileSetItem.appendRow(fileItem)
        self._model.appendRow(multiFileSetItem)

    def _itemChanged(self, item) -> None:
        with DbSession() as session:
            # TODO: Item has a registered model, not an SQL model to how do
            # we update it using the session?
            # Perhaps implement Saver and Deleter classes (next to Loader)?
            pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        index = self.indexAt(event.pos())
        if index.isValid():
            globalPos = self.viewport().mapToGlobal(event.pos())
            if event.button() == Qt.RightButton:
                self._handleRightClickEvent(index, globalPos)
                return
        super(RegisteredMultiFileSetModelTreeView, self).mousePressEvent(event)
            
    def _handleRightClickEvent(self, index, globalPos) -> None:
        item = self._model.itemFromIndex(index)
        if isinstance(item, FileItem):
            menu = FileItemMenu(self, item, globalPos)
            menu.show()
        elif isinstance(item, FileSetItem):
            menu = FileSetItemMenu(self, item, globalPos)
            menu.show()
        elif isinstance(item, MultiFileSetItem):
            menu = MultiFileSetItemMenu(self, item, globalPos)
            menu.show()
        else:
            pass
