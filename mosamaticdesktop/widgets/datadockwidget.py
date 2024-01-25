from mosamaticdesktop.widgets.dockwidget import DockWidget
from mosamaticdesktop.widgets.filesettreeview import FileSetTreeView


class DataDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(DataDockWidget, self).__init__(title)
        self._treeView = None
        self.initUi()

    def initUi(self) -> None:
        self._treeView = FileSetTreeView()
        self.setWidget(self._treeView)
        self.setMinimumHeight(200)

    def treeView(self) -> FileSetTreeView:
        return self._treeView