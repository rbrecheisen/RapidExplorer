from PySide6.QtWidgets import QTabWidget, QMainWindow, QMenuBar, QMenu
from com.application.datatab import DataTab
from com.application.tasktab import TaskTab
from com.application.viewtab import ViewTab


class TabWidget(QTabWidget):

    def __init__(self, menuBar: QMenuBar) -> None:
        super(TabWidget, self).__init__()
        self._dataTab = DataTab()
        self._taskTab = TaskTab()
        self._viewTab = ViewTab()
        self._menuBar = menuBar
        self._menuBar.addMenu(self._dataTab.getMenu())
        self.addTab(self._dataTab, DataTab.TITLE)
        self.addTab(self._taskTab, TaskTab.TITLE)
        self.addTab(self._viewTab, ViewTab.TITLE)
