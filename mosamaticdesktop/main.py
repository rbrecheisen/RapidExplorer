import sys

from PySide6.QtWidgets import QApplication

# from mainwindow import MainWindow
from mosamaticdesktop.mainwindow import MainWindow

with open('VERSION') as f:
    VERSION = f.read()


def main():
    app = QApplication([])
    mainWindow = MainWindow(version=VERSION)
    mainWindow.show()
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()