import os
import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow
from logger import Logger

SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')

LOGGER = Logger()
LOGGER.info(f'SETTINGSPATH: {SETTINGSPATH}')

GITCOMMITID = os.environ.get('GITCOMMITID', None)
if not GITCOMMITID:
    os.system('echo "$(git rev-parse HEAD)" > gitcommitid.txt')
    GITCOMMITID = open('gitcommitid.txt', 'r').readline().strip()
    LOGGER.info(f'GITCOMMITID: {GITCOMMITID}')


def main():
    app = QApplication([])
    mainWindow = MainWindow(settingsPath=SETTINGSPATH)
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()