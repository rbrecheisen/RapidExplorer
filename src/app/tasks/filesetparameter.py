from typing import Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

from tasks.parameter import Parameter
from data.datamanager import DataManager


class FileSetParameter(Parameter):
    class ComboBox(QComboBox):
        def __init__(self, parent: QWidget=None) -> None:
            super(FileSetParameter.ComboBox, self).__init__(parent=parent)
            self.loadItems()

        def loadItems(self) -> None:
            self.addItem(None)
            fileSets = DataManager().fileSets()
            for fileSet in fileSets:
                self.addItem(fileSet.name())

        def showPopup(self) -> None:
            self.clear()
            self.loadItems()
            return super().showPopup()

    def __init__(self, name: str, labelText: str, optional: bool=False, visible: bool=True, defaultValue: Any=None, parent: QWidget=None) -> None:
        super(FileSetParameter, self).__init__(
            name=name, labelText=labelText, optional=optional, visible=visible, defaultValue=defaultValue, parent=parent)
        self.initUi()

    def initUi(self) -> None:
        label = QLabel(self.labelText())
        comboBox = FileSetParameter.ComboBox(self)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(comboBox)
        self.setLayout(layout)