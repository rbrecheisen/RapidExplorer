import os
import sys

from PySide6.QtWidgets import QApplication

# from mainwindow import MainWindow
from mosamaticdesktop.mainwindow import MainWindow

versionFile = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'VERSION')
with open(versionFile) as f:
    VERSION = f.read()

gitHubCommitIdFile = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'GIT_COMMIT_ID')
with open(gitHubCommitIdFile) as f:
    GIT_COMMIT_ID = f.read()


def main():
    app = QApplication([])
    mainWindow = MainWindow(version=VERSION, gitHubCommitId=GIT_COMMIT_ID)
    mainWindow.show()
    sys.exit(app.exec())
    pass


if __name__ == "__main__":
    main()