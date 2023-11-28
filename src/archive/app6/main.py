import os
import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow


def main():
    app = QApplication([])
    settingsPath = os.environ.get('SETTINGSPATH', 'settings.ini')
    mainWindow = MainWindow(settingsPath=settingsPath)
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
