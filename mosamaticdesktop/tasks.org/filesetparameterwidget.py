from typing import Any

from PySide6.QtWidgets import QWidget, QLabel, QComboBox

from mosamaticdesktop.tasks.parameter import Parameter
from mosamaticdesktop.tasks.parameterwidget import ParameterWidget
from mosamaticdesktop.data.datamanager import DataManager


class FileSetParameterWidget(ParameterWidget):
    class ComboBox(QComboBox):
        def __init__(self, parent: QWidget=None) -> None:
            super(FileSetParameterWidget.ComboBox, self).__init__(parent=parent)
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

    def __init__(self, parameter: Parameter, parent: QWidget=None) -> None:
        super(FileSetParameterWidget, self).__init__(parameter=parameter, parent=parent)
        if self.parameter().defaultValue() is not None:
            self.parameter().setValue(self.parameter().defaultValue())
        self.initUi()

    def initUi(self) -> None:
        label = QLabel(self.labelText())
        comboBox = FileSetParameterWidget.ComboBox(self)
        comboBox.currentTextChanged.connect(self.currentTextChanged)
        self.layout().addWidget(label)
        self.layout().addWidget(comboBox)

    def currentTextChanged(self, text: str) -> None:
        self.parameter().setValue(text)