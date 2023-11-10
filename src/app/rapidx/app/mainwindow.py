import os

from PySide6.QtCore import Qt, QSize, QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog
from PySide6.QtGui import QAction, QGuiApplication

from rapidx.app.plugins.pluginmanager import PluginManager
from rapidx.app.data.db.db import Db
from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfileimporter import DicomFileImporter
from rapidx.app.data.fileset.dicomfilesetimporter import DicomFileSetImporter
from rapidx.app.data.multifileset.dicommultifilesetimporter import DicomMultiFileSetImporter
from rapidx.app.widgets.datadockwidget import DataDockWidget
from rapidx.app.widgets.viewsdockwidget import ViewsDockWidget
from rapidx.app.widgets.mainviewdockwidget import MainViewDockWidget
from rapidx.app.widgets.dockwidget import DockWidget

MULTIFILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILE_PATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._dockWidgetData = None
        self._dockWidgetTasks = None
        self._dockWidgetViews = None
        self._dockWidgetMainView = None
        self._progressBarDialog = None
        self._dicomFileImporter = None
        self._dicomFileSetImporter = None
        self._dicomMultiFileSetImporter = None
        self._loadPlugins()
        self._initUi()

    def _loadPlugins(self) -> None:
        manager = PluginManager()
        manager.loadAll()

    def _initUi(self) -> None:
        self._initMenus()
        self._initDockWidgetData()
        self._initDockWidgetTasks()
        self._initDockWidgetViews()
        self._initDockWidgetMainView()
        self._initProgressBarDialog()
        self._initMainWindow()

    def _initMenus(self) -> None:
        importDicomFileAction = QAction('Import DICOM Image...', self)
        importDicomFileSetAction = QAction('Import DICOM Image Series...', self)
        importDicomMultiFileSetAction = QAction('Import Multiple DICOM Image Series...', self)
        printFileCacheToConsoleAction = QAction('Print File Cache to Console', self)
        importDicomFileAction.triggered.connect(self._importDicomFile)
        importDicomFileSetAction.triggered.connect(self._importDicomFileSet)
        importDicomMultiFileSetAction.triggered.connect(self._importDicomMultiFileSet)
        printFileCacheToConsoleAction.triggered.connect(self._printFileCacheToConsole)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self._exit)
        datasetsMenu = QMenu('Data')
        datasetsMenu.addAction(importDicomFileAction)
        datasetsMenu.addAction(importDicomFileSetAction)
        datasetsMenu.addAction(importDicomMultiFileSetAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(printFileCacheToConsoleAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(exitAction)
        self.menuBar().addMenu(datasetsMenu)
        self.menuBar().setNativeMenuBar(False)

    def _initDockWidgetData(self) -> None:
        db = Db()
        self._dockWidgetData = DataDockWidget('Data', db=db)
        db.close()
        self._dockWidgetData.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dockWidgetData)

    def _initDockWidgetTasks(self) -> None:
        self._dockWidgetTasks = DockWidget('Tasks', self)
        self._dockWidgetTasks.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dockWidgetTasks)

    def _initDockWidgetViews(self) -> None:
        self._dockWidgetViews = ViewsDockWidget('Views', self)
        self._dockWidgetViews.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockWidgetViews)

    def _initDockWidgetMainView(self) -> None:
        self._dockWidgetMainView = MainViewDockWidget('Main View', self)
        self._dockWidgetMainView.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockWidgetMainView)

    def _initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def _initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dockWidgetData, self._dockWidgetTasks, Qt.Vertical)
        self.splitDockWidget(self._dockWidgetMainView, self._dockWidgetViews, Qt.Vertical)
        self.setFixedSize(QSize(1024, 800))
        self.setWindowTitle('RapidX')
        self._centerWindow()

    def _importDicomFile(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM Image', FILE_PATH)
        if filePath:
            with Db() as db:
                self._progressBarDialog.show()
                self._progressBarDialog.setValue(0)
                self._dicomFileImporter = DicomFileImporter(path=filePath, db=db)
                self._dicomFileImporter.signal().progress.connect(self._updateProgress)
                self._dicomFileImporter.signal().finished.connect(self._importDicomFileFinished)
                QThreadPool.globalInstance().start(self._dicomFileImporter)

    def _importDicomFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESET_DIR)
        if dirPath:
            with Db() as db:
                self._progressBarDialog.show()
                self._progressBarDialog.setValue(0)
                self._dicomFileSetImporter = DicomFileSetImporter(path=dirPath, db=db)
                self._dicomFileSetImporter.signal().progress.connect(self._updateProgress)
                self._dicomFileSetImporter.signal().finished.connect(self._importDicomFileSetFinished)
                QThreadPool.globalInstance().start(self._dicomFileSetImporter)

    def _importDicomMultiFileSet(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open Multiple DICOM Image Series', MULTIFILESET_DIR)
        if dirPath:            
            db = Db()
            # self._progressBarDialog.show()
            # self._progressBarDialog.setValue(0)
            self._dicomMultiFileSetImporter = DicomMultiFileSetImporter(path=dirPath, db=db)
            self._dicomMultiFileSetImporter.signal().progress.connect(self._updateProgress)
            self._dicomMultiFileSetImporter.signal().finished.connect(self._importDicomMultiFileSetFinished)
            self._dicomMultiFileSetImporter.run()
            db.close()
            # QThreadPool.globalInstance().start(self._dicomMultiFileSetImporter)

    def _printFileCacheToConsole(self) -> None:
        cache = FileCache()
        if len(cache.data().keys()) == 0:
            print('{}')
        else:
            for k, v in cache.data().items():
                print(f'{k}: {v}')

    def _updateProgress(self, value) -> None:
        self._progressBarDialog.setValue(value)

    def _importDicomFileFinished(self, _) -> None:
        self._dockWidgetData.addData(self._dicomFileImporter.data())

    def _importDicomFileSetFinished(self, _) -> None:
        self._dockWidgetData.addData(self._dicomFileSetImporter.data())

    def _importDicomMultiFileSetFinished(self, _) -> None:
        print(f'MainWindow.importDicomMultiFileSetFinished: {self._dicomMultiFileSetImporter.data()}')
        self._dockWidgetData.addData(self._dicomMultiFileSetImporter.data())

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def _exit(self) -> None:
        QApplication.exit()

