from typing import Any, List

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QListWidget, QPushButton

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.data.datamanager import DataManager


class MultiFileSetParameter(Parameter):
    class ComboBox(QComboBox):
        def __init__(self, parent: QWidget=None) -> None:
            super(MultiFileSetParameter.ComboBox, self).__init__(parent=parent)
            self._dataManager = DataManager()
            self.loadItems()

        def loadItems(self) -> None:
            self.addItem(None)
            fileSets = self._dataManager.fileSets()
            for fileSet in fileSets:
                self.addItem(fileSet.name())

    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(MultiFileSetParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        self._fileSetComboBox = None
        self._fileSetItemListWidget = None
        self.initUi()

    def initUi(self) -> None:
        label = QLabel(self.labelText())
        self._fileSetComboBox = MultiFileSetParameter.ComboBox(self)
        addButton = QPushButton('Add', self)
        addButton.clicked.connect(self.addFileSet)
        removeButton = QPushButton('Remove', self)
        removeButton.clicked.connect(self.removeFileSet)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(removeButton)
        self._fileSetItemListWidget = QListWidget(self)
        self.layout().addWidget(label)
        self.layout().addWidget(self._fileSetComboBox)
        self.layout().addLayout(buttonLayout)
        self.layout().addWidget(self._fileSetItemListWidget)

    def addFileSet(self):
        itemNameIndex = self._fileSetComboBox.currentIndex()
        itemName = self._fileSetComboBox.itemText(itemNameIndex)
        if itemName and itemName != '':
            self._fileSetItemListWidget.addItem(itemName)
            self._fileSetComboBox.removeItem(itemNameIndex)
            self.setValue(self.items())

    def removeFileSet(self):
        item = self._fileSetItemListWidget.currentItem()
        if item:
            self._fileSetItemListWidget.takeItem(self._fileSetItemListWidget.row(item))
            self._fileSetComboBox.addItem(item.text())
            self.setValue(self.items())

    def items(self) -> List[str]:
        items = []
        for i in range(self._fileSetItemListWidget.count()):
            items.append(self._fileSetItemListWidget.item(i).text())
        return items

    def copy(self):
        return MultiFileSetParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )