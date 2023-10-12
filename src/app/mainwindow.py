from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QMenu


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._dockWidgetDatasets = None
        self._dockWidgetTasks = None
        self._dockWidgetViews = None
        self._dockWidgetMainView = None
        self._initUi()

    def _initUi(self) -> None:
        pass

    def _initMenus(self) -> None:
        pass

    def _initDockWidgets(self) -> None:
        pass

