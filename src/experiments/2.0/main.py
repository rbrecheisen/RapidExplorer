import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow
from utils import SettingsIniFile


def main():
    settingsIniFile = SettingsIniFile()
    app = QApplication([])
    mainWindow = MainWindow(settingsPath=settingsIniFile.path())
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()