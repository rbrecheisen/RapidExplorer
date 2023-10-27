import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog
from PySide6.QtGui import QAction, QGuiApplication

from rapidx.app.widgets.dockwidget import DockWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._dockWidgetData = None
        self._dockWidgetTasks = None
        self._dockWidgetViews = None
        self._dockWidgetMainView = None
        self._initUi()

    def _initUi(self) -> None:
        self._initMenus()
        self._initDockWidgetData()
        self._initDockWidgetTasks()
        self._initDockWidgetViews()
        self._initDockWidgetMainView()
        self._initMainWindow()

    def _initMenus(self) -> None:
        importDicomFileAction = QAction('Import DICOM Image...', self)
        importDicomFileAction.triggered.connect(self._importDicomFile)
        importDicomFileSetAction = QAction('Import DICOM Image Series...', self)
        importDicomFileSetAction.triggered.connect(self._importDicomFileSet)
        importDicomMultiFileSetAction = QAction('Import Multiple DICOM Image Series...', self)
        importDicomMultiFileSetAction.triggered.connect(self._importDicomMultiFileSet)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self._exit)
        datasetsMenu = QMenu('Datasets')
        datasetsMenu.addAction(importDicomFileAction)
        datasetsMenu.addAction(importDicomFileSetAction)
        datasetsMenu.addAction(importDicomMultiFileSetAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(exitAction)
        self.menuBar().addMenu(datasetsMenu)
        self.menuBar().setNativeMenuBar(False)

    def _initDockWidgetData(self) -> None:
        self._dockWidgetData = DockWidget('Data', self)
        self._dockWidgetData.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dockWidgetData)

    def _initDockWidgetTasks(self) -> None:
        self._dockWidgetTasks = DockWidget('Tasks', self)
        self._dockWidgetTasks.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dockWidgetTasks)

    def _initDockWidgetViews(self) -> None:
        self._dockWidgetViews = DockWidget('Views', self)
        self._dockWidgetViews.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockWidgetViews)

    def _initDockWidgetMainView(self) -> None:
        self._dockWidgetMainView = DockWidget('Main View', self)
        self._dockWidgetMainView.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockWidgetMainView)

    def _initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dockWidgetData, self._dockWidgetTasks, Qt.Vertical)
        self.splitDockWidget(self._dockWidgetMainView, self._dockWidgetViews, Qt.Vertical)
        self.setFixedSize(QSize(1024, 800))
        self.setWindowTitle('RAPID-X')
        self._centerWindow()

    def _importDicomFile(self) -> None:
        pass

    def _importDicomFileSet(self) -> None:
        pass

    def _importDicomMultiFileSet(self) -> None:
        pass

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def _exit(self) -> None:
        QApplication.exit()

