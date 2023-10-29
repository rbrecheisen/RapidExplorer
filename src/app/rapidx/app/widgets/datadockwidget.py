from rapidx.app.widgets.dockwidget import DockWidget
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.widgets.multifilesetmodeltreewidget import MultiFileSetModelTreeWidget


class DataDockWidget(DockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(DataDockWidget, self).__init__(title, parent=parent)
        self._treeWidget = None
        self._initUi()

    def _initUi(self) -> None:
        self._treeWidget = MultiFileSetModelTreeWidget(self)
        self.setWidget(self._treeWidget)

    def addData(self, multiFileSetModel: MultiFileSetModel) -> None:
        self._treeWidget.addData(multiFileSetModel)
