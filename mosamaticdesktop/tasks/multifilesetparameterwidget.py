from typing import Any, List

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QListWidget, QPushButton, QAbstractItemView

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget
from mosamaticdesktop.data.datamanager import DataManager


class MultiFileSetParameterWidget(ParameterWidget):
    class ListWidget(QListWidget):
        def __init__(self, loadItems=True, parent: QWidget=None) -> None:
            super(MultiFileSetParameterWidget.ListWidget, self).__init__(parent=parent)
            self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
            self._dataManager = DataManager()
            if loadItems:
                self.loadItems()

        def loadItems(self) -> None:
            fileSets = self._dataManager.fileSets()
            for fileSet in fileSets:
                self.addItem(fileSet.name())

    class ComboBox(QComboBox):
        def __init__(self, parent: QWidget=None) -> None:
            super(MultiFileSetParameterWidget.ComboBox, self).__init__(parent=parent)
            self._dataManager = DataManager()
            self.loadItems()

        def loadItems(self) -> None:
            self.addItem(None)
            fileSets = self._dataManager.fileSets()
            for fileSet in fileSets:
                self.addItem(fileSet.name())

    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(MultiFileSetParameterWidget, self).__init__(parameter=parameter, parent=parent)
        self._fileSetComboBox = None
        self._fileSetSelectionListWidget = None
        self._fileSetItemListWidget = None
        self.initUi()

    def initUi(self) -> None:
        label = QLabel(self.parameter().labelText())
        self._fileSetComboBox = MultiFileSetParameterWidget.ComboBox(self)
        self._fileSetSelectionListWidget = MultiFileSetParameterWidget.ListWidget(self)
        # self._fileSetItemListWidget = QListWidget(self)
        self._fileSetItemListWidget = MultiFileSetParameterWidget.ListWidget(False, self)
        addButton = QPushButton('Add', self)
        # addButton.clicked.connect(self.addFileSet)
        addButton.clicked.connect(self.addSelectedFileSets)
        removeButton = QPushButton('Remove', self)
        # removeButton.clicked.connect(self.removeFileSet)
        removeButton.clicked.connect(self.removeSelectedFileSets)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(removeButton)
        self.layout().addWidget(label)
        # self.layout().addWidget(self._fileSetComboBox)
        self.layout().addWidget(self._fileSetSelectionListWidget)
        self.layout().addLayout(buttonLayout)
        self.layout().addWidget(self._fileSetItemListWidget)

    def addFileSet(self):
        itemNameIndex = self._fileSetComboBox.currentIndex()
        itemName = self._fileSetComboBox.itemText(itemNameIndex)
        if itemName and itemName != '':
            self._fileSetItemListWidget.addItem(itemName)
            self._fileSetComboBox.removeItem(itemNameIndex)
            self.parameter().setValue(self.items())

    def addSelectedFileSets(self) -> None:
        selectedItems = self._fileSetSelectionListWidget.selectedItems()
        if len(selectedItems) > 0:
            for selectedItem in selectedItems:
                self._fileSetItemListWidget.addItem(selectedItem.text())
                self._fileSetSelectionListWidget.takeItem(self._fileSetSelectionListWidget.row(selectedItem))
            self.parameter().setValue(self.items())

    def removeFileSet(self):
        item = self._fileSetItemListWidget.currentItem()
        if item:
            self._fileSetItemListWidget.takeItem(self._fileSetItemListWidget.row(item))
            self._fileSetSelectionListWidget.addItem(item.text())
            # self._fileSetComboBox.addItem(item.text())
            self.parameter().setValue(self.items())

    def removeSelectedFileSets(self) -> None:
        selectedItems = self._fileSetItemListWidget.selectedItems()
        if len(selectedItems) > 0:
            for selectedItem in selectedItems:
                self._fileSetItemListWidget.takeItem(self._fileSetItemListWidget.row(selectedItem))
                self._fileSetSelectionListWidget.addItem(selectedItem.text())            
            self.parameter().setValue(self.items())

    def items(self) -> List[str]:
        items = []
        for i in range(self._fileSetItemListWidget.count()):
            items.append(self._fileSetItemListWidget.item(i).text())
        return items