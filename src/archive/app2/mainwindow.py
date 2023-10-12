from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QMenu

from widgets.datasetdockwidget import DatasetDockWidget
from widgets.taskdockwidget import TaskDockWidget
from widgets.logdockwidget import LogDockWidget


class MainWindow(QMainWindow):

    MAINWINDOW_TITLE = 'Rbeesoft RAPID-Xplorer'
    MAINWINDOW_WIDTH = 1200
    MAINWINDOW_HEIGHT = 800
    MAINWINDOW_DOCK_WIDGET_DATASET_TITLE = 'Datasets'
    MAINWINDOW_DOCK_WIDGET_DATASET_WIDTH_MIN = 450
    MAINWINDOW_DOCK_WIDGET_DATASET_WIDTH_MAX = 600
    MAINWINDOW_DOCK_WIDGET_TASK_TITLE = 'Tasks'
    MAINWINDOW_DOCK_WIDGET_TASK_WIDTH_MIN = 450
    MAINWINDOW_DOCK_WIDGET_TASK_WIDTH_MAX = 600
    MAINWINDOW_DOCK_WIDGET_LOG_TITLE = 'Logs'
    MAINWINDOW_DOCK_WIDGET_LOG_HEIGHT_MIN = 100
    MAINWINDOW_DOCK_WIDGET_LOG_HEIGHT_MAX = 100
    MENU_DATASETS_TITLE = 'Data'

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.dockWidgetDatasets = None
        self.dockWidgetTasks = None
        self.dockWidgetLog = None
        self.initUi()

    def initUi(self) -> None:
        self.initMenus()
        self.initViewWidget()
        self.initDatasetWidget()
        self.initTaskWidget()
        self.initLogWidget()
        self.splitDockWidget(self.dockWidgetDatasets, self.dockWidgetTasks, Qt.Vertical)
        self.setFixedSize(QSize(MainWindow.MAINWINDOW_WIDTH, MainWindow.MAINWINDOW_HEIGHT))
        self.setWindowTitle(MainWindow.MAINWINDOW_TITLE)
        self.centerWindow()

    def initMenus(self) -> None:
        loadDicomImageAction = QAction('Load DICOM Image...', self)
        loadDicomImageAction.triggered.connect(self.loadDicomImage)
        loadDicomImageSeriesAction = QAction('Load DICOM Image Series...', self)
        loadDicomImageSeriesAction.triggered.connect(self.loadDicomImageSeries)
        loadMultiDicomImageSeriesAction = QAction('Load Multiple DICOM Image Series...', self)
        loadMultiDicomImageSeriesAction.triggered.connect(self.loadMultiDicomImageSeries)
        loadNiftiVolumeAction = QAction('Load NIFTI Volume...', self)
        loadNiftiVolumeAction.triggered.connect(self.loadNiftiVolume)
        loadMultiNiftiVolumeAction = QAction('Load Multiple NIFTI Volumes...', self)
        loadMultiNiftiVolumeAction.triggered.connect(self.loadMultiNiftiVolumes)
        loadPngImageAction = QAction('Load PNG Image...', self)
        loadPngImageAction.triggered.connect(self.loadPngImage)
        loadJpgImageAction = QAction('Load JPG Image...', self)
        loadJpgImageAction.triggered.connect(self.loadJpgImage)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.exit)
        datasetsMenu = QMenu(MainWindow.MENU_DATASETS_TITLE)
        datasetsMenu.addAction(loadDicomImageAction)
        datasetsMenu.addAction(loadDicomImageSeriesAction)
        datasetsMenu.addAction(loadMultiDicomImageSeriesAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(loadNiftiVolumeAction)
        datasetsMenu.addAction(loadMultiNiftiVolumeAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(loadPngImageAction)
        datasetsMenu.addAction(loadJpgImageAction)
        datasetsMenu.addSeparator()
        datasetsMenu.addAction(exitAction)
        self.menuBar().addMenu(datasetsMenu)
        self.menuBar().setNativeMenuBar(False)

    def initViewWidget(self) -> None:
        canvas = QLabel('Image viewer')
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def initDatasetWidget(self) -> None:
        self.dockWidgetDatasets = DatasetDockWidget(
            MainWindow.MAINWINDOW_DOCK_WIDGET_DATASET_TITLE,
            MainWindow.MAINWINDOW_DOCK_WIDGET_DATASET_WIDTH_MIN,
            MainWindow.MAINWINDOW_DOCK_WIDGET_DATASET_WIDTH_MAX,
        )
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetDatasets)

    def initTaskWidget(self) -> None:
        self.dockWidgetTasks = TaskDockWidget(
            MainWindow.MAINWINDOW_DOCK_WIDGET_TASK_TITLE,
            MainWindow.MAINWINDOW_DOCK_WIDGET_TASK_WIDTH_MIN,
            MainWindow.MAINWINDOW_DOCK_WIDGET_TASK_WIDTH_MAX,
        )
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetTasks)

    def initLogWidget(self) -> None:
        self.dockWidgetLog = LogDockWidget(
            MainWindow.MAINWINDOW_DOCK_WIDGET_LOG_TITLE,
            MainWindow.MAINWINDOW_DOCK_WIDGET_LOG_HEIGHT_MIN,
            MainWindow.MAINWINDOW_DOCK_WIDGET_LOG_HEIGHT_MAX,
        )
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidgetLog)
        self.dockWidgetLog.resize(self.dockWidgetLog.width(), self.dockWidgetLog.minimumHeight())

    def initToolBar(self) -> None:
        toolbar = QToolBar()
        action1 = QAction(QIcon(QPixmap('')), 'Action 1', self)
        action2 = QAction(QIcon(QPixmap('')), 'Action 2', self)
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def initStatusBar(self) -> None:
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

    def centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))

    # Event handlers

    def loadDicomImage(self) -> None:
        pass

    def loadDicomImageSeries(self) -> None:
        pass

    def loadMultiDicomImageSeries(self) -> None:
        pass

    def loadNiftiVolume(self) -> None:
        pass

    def loadMultiNiftiVolumes(self) -> None:
        pass

    def loadPngImage(self) -> None:
        pass

    def loadJpgImage(self) -> None:
        pass

    def exit(self) -> None:
        QApplication.exit()
