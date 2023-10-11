import os

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget, QMessageBox

from datasetbuilder import DatasetBuilder
from loaders.dicomfileloader import DicomFileLoader
from loaders.dicomfilesetloader import DicomFileSetLoader
from loaders.dicomdatasetloader import DicomDatasetLoader


DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILE_PATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')
DATASET_NAME = 'myDataset'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)
        self.button1 = QPushButton("Load DICOM Image")
        self.button2 = QPushButton("Load DICOM Image Series")
        self.button3 = QPushButton("Load Multiple DICOM Image Series")
        self.button1.clicked.connect(self.loadDicomImage)
        self.button2.clicked.connect(self.loadDicomImageSeries)
        self.button3.clicked.connect(self.loadMultipleDicomImageSeries)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle('RAPID-X')

    def loadDicomImage(self):
        self.progressBar.setValue(0)
        loader = DicomFileLoader(path=FILE_PATH)
        loader.signal().done.connect(self.loadFinished)
        loader.signal().progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(loader)

    def loadDicomImageSeries(self):
        self.progressBar.setValue(0)
        builder = DatasetBuilder(path=DATASET_DIR, name=DATASET_NAME)
        dataset = builder.build()
        loader = DicomFileSetLoader(dataset=dataset)
        loader._signal.done.connect(self.loadFinished)
        loader._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(loader)

    def loadMultipleDicomImageSeries(self):
        self.progressBar.setValue(0)
        builder = DatasetBuilder(path=DATASET_DIR, name=DATASET_NAME)
        dataset = builder.build()
        loader = DicomDatasetLoader(dataset=dataset)
        loader._signal.done.connect(self.loadFinished)
        loader._signal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(loader)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def loadFinished(self, value):
        QMessageBox.information(self, '', 'Finished')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
