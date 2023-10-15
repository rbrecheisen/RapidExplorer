import os

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget,
    QFileDialog,
)

from app.dicomfileimporter import DicomFileImporter
from app.dicomfilesetimporter import DicomFileSetImporter
from app.dicomdatasetimporter import DicomDatasetImporter
from app.datasettreewidget import DatasetTreeWidget

DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILE_PATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dicomFileImporter = None
        self.dicomFileSetImporter = None
        self.dicomDatasetImporter = None
        layout = QVBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)
        self.button1 = QPushButton("Import DICOM Image")
        self.button2 = QPushButton("Import DICOM Image Series")
        self.button3 = QPushButton("Import Multiple DICOM Image Series")
        self.button1.clicked.connect(self.importDicomFile)
        self.button2.clicked.connect(self.importDicomFileSet)
        self.button3.clicked.connect(self.importMultipleDicomDataset)
        self.treeWidget = DatasetTreeWidget(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.treeWidget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle('RAPID-X')

    def importDicomFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open DICOM File', FILE_PATH)
        if filePath:
            self.progressBar.setValue(0)
            self.dicomFileImporter = DicomFileImporter(path=filePath)
            self.dicomFileImporter.signal().done.connect(self.importDicomFileFinished)
            self.dicomFileImporter.signal().progress.connect(self.updateProgress)
            QThreadPool.globalInstance().start(self.dicomFileImporter)

    def importDicomFileSet(self):
        dirPath = QFileDialog.getExistingDirectory(self, 'Open Directory with DICOM Series', FILESET_DIR)
        if dirPath:
            self.progressBar.setValue(0)
            self.dicomFileSetImporter = DicomFileSetImporter(path=dirPath)
            self.dicomFileSetImporter._signal.done.connect(self.importDicomFileSetFinished)
            self.dicomFileSetImporter._signal.progress.connect(self.updateProgress)
            QThreadPool.globalInstance().start(self.dicomFileSetImporter)

    def importMultipleDicomDataset(self):
        dirPath = QFileDialog.getExistingDirectory(self, 'Open Directory with Multiple DICOM Series', DATASET_DIR)
        if dirPath:
            self.progressBar.setValue(0)
            self.dicomDatasetImporter = DicomDatasetImporter(path=DATASET_DIR)
            self.dicomDatasetImporter._signal.done.connect(self.importDicomDatasetFinished)
            self.dicomDatasetImporter._signal.progress.connect(self.updateProgress)
            QThreadPool.globalInstance().start(self.dicomDatasetImporter)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def importDicomFileFinished(self, value):
        self.treeWidget.addDataset(self.dicomFileImporter.data())

    def importDicomFileSetFinished(self, value):
        self.treeWidget.addDataset(self.dicomFileSetImporter.data())

    def importDicomDatasetFinished(self, value):
        self.treeWidget.addDataset(self.dicomDatasetImporter.data())


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
