import sys

from PySide6.QtWidgets import QApplication

# from mainwindow import MainWindow
from mosamaticdesktop.mainwindow import MainWindow


def main():
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()