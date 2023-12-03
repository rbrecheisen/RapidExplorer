from widgets.dockwidget import DockWidget
from widgets.filesettreeview import FileSetTreeView
from data.fileset import FileSet


class DataDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(DataDockWidget, self).__init__(title)
        self._treeView = None
        self.initUi()

    def initUi(self) -> None:
        self._treeView = FileSetTreeView()
        self.setWidget(self._treeView)
        self.setMinimumHeight(200)

    def addFileSet(self, fileSet: FileSet) -> None:
        self._treeView.addFileSet(fileSet=fileSet)

    def clearFileSets(self) -> None:
        self._treeView.clearFileSets()