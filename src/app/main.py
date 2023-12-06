import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow
from utils import SettingsIniFile
# from logger import Logger

# SETTINGSPATH = os.environ.get('SETTINGSPATH', 'settings.ini')
# SETTINGSFILEPATH = 'settings.ini'

# LOGGER = Logger()
# LOGGER.info(f'SETTINGSPATH: {SETTINGSPATH}')

# GITCOMMITID = os.environ.get('GITCOMMITID', None)
# if not GITCOMMITID:
#     os.system('echo "$(git rev-parse HEAD)" > gitcommitid.txt')
#     GITCOMMITID = open('gitcommitid.txt', 'r').readline().strip()
#     LOGGER.info(f'GITCOMMITID: {GITCOMMITID}')


def main():
    settingsIniFile = SettingsIniFile()
    app = QApplication([])
    mainWindow = MainWindow(settingsPath=settingsIniFile.path())
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()