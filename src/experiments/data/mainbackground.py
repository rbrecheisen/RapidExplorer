import os
import time

from PySide6.QtCore import Qt, QThreadPool, QRunnable
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget

from models.basemodel import BaseModel
from datasetbuilder import DatasetBuilder
from dicomimageloader import DicomImageLoader
from dicomimageseriesloader import DicomImageSeriesLoader
from multidicomimageseriesloader import MultiDicomImageSeriesLoader
from signals.fileloaderprogresssignal import FileLoaderProgressSignal


DATASET_DIR = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
DATASET_NAME = 'myDataset'


class FileLoader(QRunnable):
    def __init__(self, dataset=None):
        super(FileLoader, self).__init__()
        self.dataset = dataset
        self.progressSignal = FileLoaderProgressSignal()

    def run(self):
        imageSeriesLoader = DicomImageSeriesLoader(self.dataset, self.progressSignal)
        imageSeriesLoader.load()
        print('Done')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)
        self.button = QPushButton("Load DICOM Series")
        self.button.clicked.connect(self.loadFiles)
        layout.addWidget(self.button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def loadFiles(self):
        builder = DatasetBuilder(path=DATASET_DIR, name=DATASET_NAME)
        dataset = builder.build()
        fileLoader = FileLoader(dataset=dataset)
        fileLoader.progressSignal.progress.connect(self.updateProgress)
        QThreadPool.globalInstance().start(fileLoader)

    def updateProgress(self, value):
        self.progressBar.setValue(value)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
