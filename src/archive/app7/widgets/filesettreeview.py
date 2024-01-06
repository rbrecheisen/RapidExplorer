from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QMouseEvent

from data.datamanager import DataManager
from data.fileset import FileSet
from widgets.fileitem import FileItem
from widgets.fileitemmenu import FileItemMenu
from widgets.filesetitem import FileSetItem
from widgets.filesetitemmenu import FileSetItemMenu


class FileSetTreeView(QTreeView):
    def __init__(self) -> None:
        super(FileSetTreeView, self).__init__()
        self._model = None
        self._dataManager = DataManager()
        self.initModel()
        self.loadFileSetsFromDatabase()

    def initModel(self) -> None:
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['File Sets'])
        self._model.itemChanged.connect(self.itemChanged)
        self.setModel(self._model)

    def itemChanged(self, item: QStandardItem) -> None:
        if isinstance(item, FileSetItem):
            fileSet = item.fileSet()
            fileSet.setName(item.text())
            self._dataManager.updateFileSet(fileSet=fileSet)
        else:
            pass

    def addFileSet(self, fileSet: FileSet) -> None:
        fileSetItem = FileSetItem(fileSet=fileSet)
        fileSetItem.setEditable(False)
        for file in fileSet.files():
            fileItem = FileItem(file=file)
            fileItem.setEditable(False)
            fileSetItem.appendRow(fileItem)
        self._model.appendRow(fileSetItem)

    def loadFileSetsFromDatabase(self) -> None:
        for fileSet in self._dataManager.fileSets():
            self.addFileSet(fileSet=fileSet)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        index = self.indexAt(event.pos())
        if index.isValid():
            globalPos = self.viewport().mapToGlobal(event.pos())
            if event.button() == Qt.RightButton:
                self.rightClickEvent(index, globalPos)
                return
        super(FileSetTreeView, self).mousePressEvent(event)

    def rightClickEvent(self, index: int, globalPos: QPoint) -> None:
        item = self._model.itemFromIndex(index)
        if isinstance(item, FileItem):
            menu = FileItemMenu(self, item, globalPos)
            menu.show()
        elif isinstance(item, FileSetItem):
            menu = FileSetItemMenu(self, item, globalPos)
            menu.show()
        else:
            pass

    def clearFileSets(self) -> None:
        self._model.clear()