from PySide6.QtWidgets import QMainWindow

from logger import Logger

LOGGER = Logger()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        LOGGER.info('Initializing main window...')