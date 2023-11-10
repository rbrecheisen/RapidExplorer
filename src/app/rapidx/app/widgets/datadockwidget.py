from rapidx.app.data.db.db import Db
from rapidx.app.widgets.dockwidget import DockWidget
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.widgets.tree.multifilesetmodeltreewidget import MultiFileSetModelTreeWidget


class DataDockWidget(DockWidget):
    def __init__(self, title: str, db: Db) -> None:
        super(DataDockWidget, self).__init__(title)
        self._db = db
        self._treeWidget = None
        self._initUi()

    def _initUi(self) -> None:
        self._treeWidget = MultiFileSetModelTreeWidget(db=self._db)
        self.setWidget(self._treeWidget)

    def treeWidget(self):
        return self._treeWidget

    def addData(self, multiFileSetModel: MultiFileSetModel) -> None:
        self._treeWidget.addData(multiFileSetModel)
