import os
import sys

from PySide6.QtWidgets import QApplication

# from mainwindow import MainWindow
from mosamaticdesktop.mainwindow import MainWindow

versionFile = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'VERSION')
print(versionFile)
with open(versionFile) as f:
    VERSION = f.read()


def main():
    app = QApplication([])
    mainWindow = MainWindow(version=VERSION)
    mainWindow.show()
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()