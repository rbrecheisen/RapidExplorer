import time

from PySide6.QtCore import Qt, QThreadPool, QRunnable, Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget

class Signals(QObject):
    progress = Signal(int)

class FileLoader(QRunnable):
    def __init__(self, file_list=None):
        super(FileLoader, self).__init__()
        self.file_list = file_list
        self.signals = Signals()

    def run(self):
        steps = 5
        for i in range(steps):
            print(f'Loading file {i}...')
            time.sleep(2)
            progress = int((i + 1) / steps * 100)
            self.signals.progress.emit(progress)
        print('Done')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.button = QPushButton("Load Files")
        self.button.clicked.connect(self.load_files)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_files(self):
        file_list = ["file1.txt", "file2.txt", "file3.txt"]  # Replace with your actual file list

        file_loader = FileLoader(file_list)
        file_loader.signals.progress.connect(self.update_progress)
        
        QThreadPool.globalInstance().start(file_loader)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
