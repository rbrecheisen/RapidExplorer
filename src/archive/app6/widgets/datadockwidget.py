from widgets.dockwidget import DockWidget
from widgets.registeredmultifilesetmodeltreeview import RegisteredMultiFileSetModelTreeView


class DataDockWidget(DockWidget):
    def __init__(self, title: str) -> None:
        super(DataDockWidget, self).__init__(title)
        self._treeView = None
        self._initUi()

    def _initUi(self) -> None:
        self._treeView = RegisteredMultiFileSetModelTreeView()
        self.setWidget(self._treeView)
        self.setMinimumHeight(200)

    def treeView(self) -> RegisteredMultiFileSetModelTreeView:
        return self._treeView
    
    def clearData(self) -> None:
        self._treeView.clearData()