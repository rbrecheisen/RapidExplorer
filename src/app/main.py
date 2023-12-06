import os
import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow
from logger import Logger

SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')
LOGGER = Logger()
LOGGER.info(f'SETTINGSPATH: {SETTINGSPATH}')


def main():
    app = QApplication([])
    mainWindow = MainWindow(settingsPath=SETTINGSPATH)
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()