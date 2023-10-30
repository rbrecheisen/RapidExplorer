from PySide6.QtWidgets import QDockWidget, QListWidget, QListWidgetItem, QSizePolicy

from rapidx.app.dockwidget import Dockwidget


class MainViewDockWidget(Dockwidget):
    def __init__(self, title: str, parent=None) -> None:
        super(MainViewDockWidget, self).__init__(title, parent=parent)
        self._initUi()

    def _initUi(self) -> None:
        # listWidget = QListWidget()
        # listWidget.addItem(QListWidgetItem('Dataset 1'))
        # listWidget.addItem(QListWidgetItem('Dataset 2'))
        # listWidget.addItem(QListWidgetItem('Dataset 3'))
        # self.setWidget(listWidget)
        pass