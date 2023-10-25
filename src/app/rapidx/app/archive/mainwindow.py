import os

from PySide6.QtCore import Qt, QThreadPool, QSize, QTimer
from PySide6.QtGui import QGuiApplication, QAction, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplashScreen, QWidget, QFileDialog, QMenu, QProgressDialog, 
)

from rapidx.app.dicomfileimporter import DicomFileImporter
from rapidx.app.dicomfilesetimporter import DicomFileSetImporter
from rapidx.app.dicomdatasetimporter import DicomDatasetImporter
from rapidx.app.datasetsdockwidget import DatasetsDockWidget
from rapidx.app.tasksdockwidget import TasksDockWidget
from rapidx.app.viewsdockwidget import ViewsDockWidget
from rapidx.app.mainviewdockwidget import MainViewDockWidget

DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILE_PATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._dockWidgetDatasets = None
        self._dockWidgetTasks = None
        self._dockWidgetMainView = None
        self._dockWidgetViews = None
        self._dicomFileImporter = None
        self._dicomFileSetImporter = None
        self._dicomDatasetImporter = None
        self._progressBarDialog = None
        self._initUi()

    def _initUi(self) -> None:
        self._initMenus()
        self._initDockWidgetDatasets()
        self._initDockWidgetTasks()
        self._initDockWidgetMainView()
        self._initDockWidgetViews()
        self._initProgressBarDialog()
        self._initMainWindow()

    def _initMenus(self) -> None:
        importDicomImageAction = QAction('Import DICOM Image...', self)
        importDicomImageAction.triggered.connect(self._importDicomImage)
        importDicomImageSeriesAction = QAction('Import DICOM Image Series...', self)
        importDicomImageSeriesAction.triggered.connect(self._importDicomImageSeries)
        importMultiDicomImageSeriesAction = QAction('Import Multiple DICOM Image Series...', self)
        importMultiDicomImageSeriesAction.triggered.connect(self._importMultiDicomImageSeries)
        importNiftiVolumeAction = QAction('Import NIFTI Volume...', self)
        importNiftiVolumeAction.triggered.connect(self._importNiftiVolume)
        importMultiNiftiVolumeAction = QAction('Import Multiple NIFTI Volumes...', self)
        importMultiNiftiVolumeAction.triggered.connect(self._importMultiNiftiVolumes)
        importPngImageAction = QAction('Import PNG Image...', self)
        importPngImageAction.triggered.connect(self._importPngImage)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self._exit)
        datasetsMenu = QMenu('Datasets')
        datasetsMenu.addAction(importDicomImageAction)
        datasetsMenu.addAction(importDicomImageSeriesAction)
        datasetsMenu.addAction(importMultiDicomImageSeriesAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(importNiftiVolumeAction)
        datasetsMenu.addAction(importMultiNiftiVolumeAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(importPngImageAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(exitAction)
        self.menuBar().addMenu(datasetsMenu)
        self.menuBar().setNativeMenuBar(False)

    def _initDockWidgetDatasets(self) -> None:
        self._dockWidgetDatasets = DatasetsDockWidget('Dataset Explorer', self)
        self._dockWidgetDatasets.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dockWidgetDatasets)

    def _initDockWidgetTasks(self) -> None:
        self._dockWidgetTasks = TasksDockWidget('Tasks', self)
        self._dockWidgetTasks.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dockWidgetTasks)

    def _initDockWidgetMainView(self) -> None:
        self._dockWidgetMainView = MainViewDockWidget('Main View', self)
        self._dockWidgetMainView.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockWidgetMainView)

    def _initDockWidgetViews(self) -> None:
        self._dockWidgetViews = ViewsDockWidget('Views', self)
        self._dockWidgetViews.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dockWidgetViews)

    def _initProgressBarDialog(self) -> None:
        self._progressBarDialog = QProgressDialog('Importing Files...', 'Abort Import', 0, 100, self)
        self._progressBarDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self._progressBarDialog.setAutoReset(True)
        self._progressBarDialog.setAutoClose(True)
        self._progressBarDialog.close()

    def _initMainWindow(self) -> None:
        self.setCentralWidget(QWidget(self))
        self.centralWidget().hide()
        self.splitDockWidget(self._dockWidgetDatasets, self._dockWidgetTasks, Qt.Vertical)
        self.splitDockWidget(self._dockWidgetMainView, self._dockWidgetViews, Qt.Vertical)
        self.setFixedSize(QSize(1024, 800))
        self.setWindowTitle('RAPID-X')
        self._centerWindow()

    # Import handlers

    def _importDicomImage(self) -> None:
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM Image', FILE_PATH)
        if filePath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dicomFileImporter = DicomFileImporter(path=filePath)
            self._dicomFileImporter.signal().done.connect(self._importDicomFileFinished)
            self._dicomFileImporter.signal().progress.connect(self._updateProgress)
            QThreadPool.globalInstance().start(self._dicomFileImporter)

    def _importDicomImageSeries(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open DICOM Image Series', FILESET_DIR)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dicomFileSetImporter = DicomFileSetImporter(path=dirPath)
            self._dicomFileSetImporter.signal().done.connect(self._importDicomFileSetFinished)
            self._dicomFileSetImporter.signal().progress.connect(self._updateProgress)
            QThreadPool.globalInstance().start(self._dicomFileSetImporter)

    def _importMultiDicomImageSeries(self) -> None:
        dirPath = QFileDialog.getExistingDirectory(self, 'Open Multiple DICOM Image Series', DATASET_DIR)
        if dirPath:
            self._progressBarDialog.show()
            self._progressBarDialog.setValue(0)
            self._dicomDatasetImporter = DicomDatasetImporter(path=dirPath)
            self._dicomDatasetImporter.signal().done.connect(self._importDicomDatasetFinished)
            self._dicomDatasetImporter.signal().progress.connect(self._updateProgress)
            QThreadPool.globalInstance().start(self._dicomDatasetImporter)

    def _importNiftiVolume(self) -> None:
        pass

    def _importMultiNiftiVolumes(self) -> None:
        pass

    def _importPngImage(self) -> None:
        pass

    # Import finished handlers

    def _importDicomFileFinished(self, _) -> None:
        self._dockWidgetDatasets.addDataset(self._dicomFileImporter.data())

    def _importDicomFileSetFinished(self, _) -> None:
        self._dockWidgetDatasets.addDataset(self._dicomFileSetImporter.data())

    def _importDicomDatasetFinished(self, _) -> None:
        self._dockWidgetDatasets.addDataset(self._dicomDatasetImporter.data())

    def _updateProgress(self, value) -> None:
        self._progressBarDialog.setValue(value)

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    def _exit(self) -> None:
        QApplication.exit()


# class MainWindow2(QMainWindow):
#     def __init__(self):
#         super(MainWindow2, self).__init__()
#         self.dicomFileImporter = None
#         self.dicomFileSetImporter = None
#         self.dicomDatasetImporter = None
#         layout = QVBoxLayout()
#         self.progressBar = QProgressBar()
#         self.progressBar.setValue(0)
#         layout.addWidget(self.progressBar)
#         self.button1 = QPushButton("Import DICOM Image")
#         self.button2 = QPushButton("Import DICOM Image Series")
#         self.button3 = QPushButton("Import Multiple DICOM Image Series")
#         self.button1.clicked.connect(self.importDicomFile)
#         self.button2.clicked.connect(self.importDicomFileSet)
#         self.button3.clicked.connect(self.importMultipleDicomDataset)
#         self.treeWidget = DatasetTreeWidget(self)
#         layout.addWidget(self.button1)
#         layout.addWidget(self.button2)
#         layout.addWidget(self.button3)
#         layout.addWidget(self.treeWidget)
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)
#         self.setWindowTitle('RAPID-X')

#     def importDicomFile(self):
#         filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM File', FILE_PATH)
#         if filePath:
#             self.progressBar.setValue(0)
#             self.dicomFileImporter = DicomFileImporter(path=filePath)
#             self.dicomFileImporter.signal().done.connect(self.importDicomFileFinished)
#             self.dicomFileImporter.signal().progress.connect(self.updateProgress)
#             QThreadPool.globalInstance().start(self.dicomFileImporter)

#     def importDicomFileSet(self):
#         dirPath = QFileDialog.getExistingDirectory(self, 'Open Directory with DICOM Series', FILESET_DIR)
#         if dirPath:
#             self.progressBar.setValue(0)
#             self.dicomFileSetImporter = DicomFileSetImporter(path=dirPath)
#             self.dicomFileSetImporter._signal.done.connect(self.importDicomFileSetFinished)
#             self.dicomFileSetImporter._signal.progress.connect(self.updateProgress)
#             QThreadPool.globalInstance().start(self.dicomFileSetImporter)

#     def importMultipleDicomDataset(self):
#         dirPath = QFileDialog.getExistingDirectory(self, 'Open Directory with Multiple DICOM Series', DATASET_DIR)
#         if dirPath:
#             self.progressBar.setValue(0)
#             self.dicomDatasetImporter = DicomDatasetImporter(path=DATASET_DIR)
#             self.dicomDatasetImporter._signal.done.connect(self.importDicomDatasetFinished)
#             self.dicomDatasetImporter._signal.progress.connect(self.updateProgress)
#             QThreadPool.globalInstance().start(self.dicomDatasetImporter)

#     def updateProgress(self, value):
#         self.progressBar.setValue(value)

#     def importDicomFileFinished(self, value):
#         self.treeWidget.addDataset(self.dicomFileImporter.data())

#     def importDicomFileSetFinished(self, value):
#         self.treeWidget.addDataset(self.dicomFileSetImporter.data())

#     def importDicomDatasetFinished(self, value):
#         self.treeWidget.addDataset(self.dicomDatasetImporter.data())


# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec()
