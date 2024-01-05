from PySide6.QtCore import Qt, QSize, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog, QMessageBox
from PySide6.QtGui import QAction, QGuiApplication

from widgets.datadockwidget import DataDockWidget
from widgets.viewersdockwidget import ViewersDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.mainviewerdockwidget import MainViewerDockWidget

WINDOWTITLE = 'Mosamatic Desktop 2.0'


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._mainViewDockWidget = None
        self._viewsDockWidget = None
        self.initUi()

    def initUi(self) -> None:
        self.initDataDockWidget()
        self.initTaskDockWidget()
        self.initMainViewerDockWidget()
        self.initViewersDockWidget()
        self.initMainWindow()

    def initDataDockWidget(self) -> None:
        self._dataDockWidget = DataDockWidget(title='Data')
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget(title='Tasks')
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def initMainViewerDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewerDockWidget(title='Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def initViewersDockWidget(self) -> None:
        self._viewsDockWidget = ViewersDockWidget(title='Views')
        self._viewsDockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._viewsDockWidget)

    def initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        self.splitDockWidget(self._mainViewDockWidget, self._viewsDockWidget, Qt.Vertical)
        self.setWindowTitle(WINDOWTITLE)
        self.centerWindow()

    def centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))