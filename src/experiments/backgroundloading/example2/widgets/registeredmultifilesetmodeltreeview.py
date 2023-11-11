from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItemModel, QMouseEvent

from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel
from widgets.multifilesetitem import MultiFileSetItem
from widgets.filesetitem import FileSetItem
from widgets.fileitem import FileItem


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
        if isinstance(item, FileSetItem):
            pass
        elif isinstance(item, MultiFileSetItem):
            pass
        else:
            pass
