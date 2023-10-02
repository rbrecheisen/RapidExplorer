from PySide6.QtWidgets import QTabWidget, QMainWindow, QMenuBar, QMenu
from com.application.tab.datatab import DataTab
from com.application.tab.tasktab import TaskTab
from com.application.tab.viewtab import ViewTab


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
