from PySide6.QtWidgets import QWidget

from rapidx.app.dockwidget import Dockwidget


class TasksDockWidget(Dockwidget):
    def __init__(self, title: str, parent=None) -> None:
        super(TasksDockWidget, self).__init__(title, parent=parent)
        self._initUi()

    def _initUi(self) -> None:
        # listWidget = QListWidget()
        # listWidget.addItem(QListWidgetItem('Task 1'))
        # listWidget.addItem(QListWidgetItem('Task 2'))
        # listWidget.addItem(QListWidgetItem('Task 3'))
        # self.setWidget(listWidget)
        self.setWidget(QWidget(self))
        pass