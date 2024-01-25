from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QResizeEvent, QStandardItemModel, QStandardItem, QMouseEvent

from mosamaticdesktop.data.datamanager import DataManager
from mosamaticdesktop.data.fileset import FileSet
from mosamaticdesktop.widgets.fileitem import FileItem
from mosamaticdesktop.widgets.fileitemmenu import FileItemMenu
from mosamaticdesktop.widgets.filesetitem import FileSetItem
from mosamaticdesktop.widgets.filesetitemmenu import FileSetItemMenu

FIRSTCOLUMNOFFSET = 100


class FileSetTreeView(QTreeView):
    def __init__(self) -> None:
        super(FileSetTreeView, self).__init__()
        self._model = None
        self._dataManager = DataManager()
        self.initModel()
        self.loadFileSetsFromDatabase()

    def initModel(self) -> None:
        self._model = QStandardItemModel()
        self._model.setHorizontalHeaderLabels(['File Sets', 'Nr. Files'])
        self._model.itemChanged.connect(self.itemChanged)
        self.setModel(self._model)

    def itemChanged(self, item: QStandardItem) -> None:
        if isinstance(item, FileSetItem):
            fileSet = item.fileSet()
            fileSet.setName(item.text())
            self._dataManager.updateFileSet(fileSet=fileSet)

    def loadFileSetsFromDatabase(self) -> None:
        self.clearFileSets()
        for fileSet in self._dataManager.fileSets():
            self.addFileSet(fileSet=fileSet)

    def addFileSet(self, fileSet: FileSet) -> None:
        fileSetItem = FileSetItem(fileSet=fileSet)
        fileSetItem.setEditable(False)
        for file in fileSet.files():
            fileItem = FileItem(file=file)
            fileItem.setEditable(False)
            fileSetItem.appendRow([fileItem, QStandardItem()])
        self._model.appendRow([fileSetItem, QStandardItem(str(fileSetItem.fileSet().nrFiles()))])

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

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.setColumnWidth(0, event.size().width() - FIRSTCOLUMNOFFSET)
        return super().resizeEvent(event)

    def clearFileSets(self) -> None:
        self._model.clear()