from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QComboBox

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.data.datamanager import DataManager


class FileSetParameter(Parameter):
    class ComboBox(QComboBox):
        def __init__(self, parent: QWidget=None) -> None:
            super(FileSetParameter.ComboBox, self).__init__(parent=parent)
            self._dataManager = DataManager()
            self.loadItems()

        def loadItems(self) -> None:
            self.addItem(None)
            fileSets = self._dataManager.fileSets()
            for fileSet in fileSets:
                self.addItem(fileSet.name())

        def showPopup(self) -> None:
            self.clear()
            self.loadItems()
            return super().showPopup()

    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(FileSetParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        if self.defaultValue() is not None:
            self.setValue(self.defaultValue())
        self.initUi()

    def initUi(self) -> None:
        label = QLabel(self.labelText())
        comboBox = FileSetParameter.ComboBox(self)
        comboBox.currentTextChanged.connect(self.currentTextChanged)
        self.layout().addWidget(label)
        self.layout().addWidget(comboBox)

    def currentTextChanged(self, text: str) -> None:
        self.setValue(text)

    def copy(self):
        return FileSetParameter(
            name=self.name(), 
            labelText=self.labelText(), 
            optional=self.optional(), 
            visible=self.visible(), 
            defaultValue=self.defaultValue()
        )