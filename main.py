import sys

from PySide6.QtWidgets import QApplication

# from mainwindow import MainWindow
from mosamaticdesktop.mainwindow import MainWindow

with open('VERSION') as f:
    VERSION = f.read()

# with open('GIT_COMMIT_ID') as f:
#     GIT_COMMIT_ID = f.read()


def main():
    app = QApplication([])
    mainWindow = MainWindow(version=VERSION, gitHubCommitId=None)
    mainWindow.show()
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()