from PySide6.QtWidgets import QDockWidget, QListWidget, QListWidgetItem, QSizePolicy
from widgets.dockwidget import Dockwidget


class TaskDockWidget(Dockwidget):
    def __init__(self, title: str, minWidth: int, maxWidth) -> None:
        super(TaskDockWidget, self).__init__(title)
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        self.initUi()

    def initUi(self) -> None:
        listWidget = QListWidget()
        listWidget.addItem(QListWidgetItem('Task 1'))
        listWidget.addItem(QListWidgetItem('Task 2'))
        listWidget.addItem(QListWidgetItem('Task 3'))
        listWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWidget(listWidget)
        self.setMinimumWidth(self.minWidth)
        self.setMaximumWidth(self.maxWidth)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)