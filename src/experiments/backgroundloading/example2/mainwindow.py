import os

from PySide6.QtCore import Qt, QSize, QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMenu, QProgressDialog
from PySide6.QtGui import QAction, QGuiApplication

from data.filecache import FileCache
from data.dicomfiletype import DicomFileType
from data.fileimporter import FileImporter
from data.filesetimporter import FileSetImporter
from data.multifilesetimporter import MultiFileSetImporter
from widgets.datadockwidget import DataDockWidget
from widgets.viewdockwidget import ViewsDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.mainviewdockwidget import MainViewDockWidget

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self._dataDockWidget = None
        self._tasksDockWidget = None
        self._viewsDockWidget = None
        self._mainViewDockWidget = None
        self._progressBarDialog = None
        self._fileImporter = None
        self._fileSetImporter = None
        self._multiFileSetImporter = None
        self._treeView = None
        # self._loadPlugins()
        self._initUi()

    def _initUi(self) -> None:
        self._initMenus()
        self._initDataDockWidget()
        self._initTaskDockWidget()
        self._initViewDockWidget()
        self._initMainViewDockWidget()
        self._initProgressBarDialog()
        self._initMainWindow()

    def _initMenus(self) -> None:
        importDicomFileAction = QAction('Import DICOM Image...', self)
        importDicomFileSetAction = QAction('Import DICOM Image Series...', self)
        importDicomMultiFileSetAction = QAction('Import Multiple DICOM Image Series...', self)
        printFileCacheAction = QAction('Print File Cache', self)
        importDicomFileAction.triggered.connect(self._importDicomFile)
        importDicomFileSetAction.triggered.connect(self._importDicomFileSet)
        importDicomMultiFileSetAction.triggered.connect(self._importDicomMultiFileSet)
        printFileCacheAction.triggered.connect(self._printFileCache)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self._exit)
        datasetsMenu = QMenu('Data')
        datasetsMenu.addAction(importDicomFileAction)
        datasetsMenu.addAction(importDicomFileSetAction)
        datasetsMenu.addAction(importDicomMultiFileSetAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(printFileCacheAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(exitAction)
        self.menuBar().addMenu(datasetsMenu)
        self.menuBar().setNativeMenuBar(False)

    def _initDataDockWidget(self) -> None:
        self._dataDockWidget = DataDockWidget('Data')
        self._dataDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataDockWidget)

    def _initTaskDockWidget(self) -> None:
        self._tasksDockWidget = TaskDockWidget('Tasks')
        self._tasksDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._tasksDockWidget)

    def _initViewDockWidget(self) -> None:
        self._viewsDockWidget = ViewsDockWidget('Views')
        self._viewsDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._viewsDockWidget)

    def _initMainViewDockWidget(self) -> None:
        self._mainViewDockWidget = MainViewDockWidget('Main View')
        self._mainViewDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._mainViewDockWidget)

    def _initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def _initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dataDockWidget, self._tasksDockWidget, Qt.Vertical)
        self.splitDockWidget(self._mainViewDockWidget, self._viewsDockWidget, Qt.Vertical)
        self.setFixedSize(QSize(1024, 800))
        self.setWindowTitle('RapidExplorer v1.0')
        self._centerWindow()

    def _importDicomFile(self):
        # Add file dialog
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._fileImporter = FileImporter(path=FILEPATH, fileType=DicomFileType())
        self._fileImporter.signal().progress.connect(self._fileImporterProgress)
        self._fileImporter.signal().success.connect(self._importerSuccess)
        QThreadPool.globalInstance().start(self._fileImporter)

    def _importDicomFileSet(self):
        # Add file dialog
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._fileSetImporter = FileSetImporter(path=FILESETPATH, fileType=DicomFileType())
        self._fileSetImporter.signal().progress.connect(self._fileSetImporterProgress)
        self._fileSetImporter.signal().success.connect(self._importerSuccess)
        QThreadPool.globalInstance().start(self._fileSetImporter)

    def _importDicomMultiFileSet(self):
        # Add file dialog
        self._progressBarDialog.show()
        self._progressBarDialog.setValue(0)
        self._multiFileSetImporter = MultiFileSetImporter(path=MULTIFILESETPATH, fileType=DicomFileType())
        self._multiFileSetImporter.signal().progress.connect(self._multiFileSetImporterProgress)
        self._multiFileSetImporter.signal().success.connect(self._importerSuccess)
        QThreadPool.globalInstance().start(self._multiFileSetImporter)

    def _fileImporterProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._fileImporter.data())

    def _fileSetImporterProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._fileSetImporter.data())

    def _multiFileSetImporterProgress(self, progress):
        self._progressBarDialog.setValue(progress)
        if progress == 100:
            self._dataDockWidget.treeView().addRegisteredMultiFileSetModel(self._multiFileSetImporter.data())

    def _importerSuccess(self, success):
        if success:
            print('success')
        else:
            print('failure')

    def _printFileCache(self):
        FileCache().printFiles()

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def _exit(self) -> None:
        QApplication.exit()