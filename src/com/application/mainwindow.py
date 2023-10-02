import resources

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QPaintEvent, QPixmap, QColor, QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu
from com.application.tabwidget import TabWidget


class MainWindow(QMainWindow):

    TITLE = 'Mosamatic Desktop'
    WIDTH = 800
    HEIGHT = 600
    BACKGROUND_IMAGE = ':/images/cachexia.png'
    BACKGROUND_GRAY_RECT_R = 255
    BACKGROUND_GRAY_RECT_G = 255
    BACKGROUND_GRAY_RECT_B = 255
    BACKGROUND_GRAY_RECT_A = 64
    
    def __init__(self):
        super(MainWindow, self).__init__()
        tabWidget = TabWidget(self.menuBar())
        self.menuBar().setNativeMenuBar(False)
        self.setCentralWidget(tabWidget)
        self.setFixedSize(QSize(MainWindow.WIDTH, MainWindow.HEIGHT))
        self.setWindowTitle(MainWindow.TITLE)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap(MainWindow.BACKGROUND_IMAGE)
        painter.drawPixmap(self.rect(), pixmap)
        painter.setBrush(QColor(
            MainWindow.BACKGROUND_GRAY_RECT_R,
            MainWindow.BACKGROUND_GRAY_RECT_G,
            MainWindow.BACKGROUND_GRAY_RECT_B,
            MainWindow.BACKGROUND_GRAY_RECT_A,
        ))
        painter.drawRect(self.rect())