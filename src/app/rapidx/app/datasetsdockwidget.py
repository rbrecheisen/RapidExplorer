from rapidx.app.dockwidget import Dockwidget
from rapidx.app.dataset import Dataset
from rapidx.app.datasettreewidget import DatasetTreeWidget


class DatasetsDockWidget(Dockwidget):
    def __init__(self, title: str, parent=None) -> None:
        super(DatasetsDockWidget, self).__init__(title, parent=parent)
        self._treeWidget = None
        self._initUi()

    def _initUi(self) -> None:
        self._treeWidget = DatasetTreeWidget(self)
        # listWidget = QListWidget()
        # listWidget.addItem(QListWidgetItem('Dataset 1'))
        # listWidget.addItem(QListWidgetItem('Dataset 2'))
        # listWidget.addItem(QListWidgetItem('Dataset 3'))
        self.setWidget(self._treeWidget)

    def addDataset(self, dataset: Dataset) -> None:
        self._treeWidget.addDataset(dataset)
