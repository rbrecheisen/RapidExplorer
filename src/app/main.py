import os
import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow
from logger import Logger


def main():
    app = QApplication([])
    settingsPath = os.environ.get('SETTINGSPATH', 'settings.ini')
    logger = Logger()
    logger.info(f'{settingsPath}')
    mainWindow = MainWindow(settingsPath=settingsPath)
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()