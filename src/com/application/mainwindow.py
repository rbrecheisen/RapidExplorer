import resources

from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QPaintEvent, QPixmap, QColor, QGuiApplication, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMessageBox

from com.application.tab.tabwidget import TabWidget


class MainWindow(QMainWindow):

    TITLE = 'Rbeesoft RAPID'
    MENU_ITEM_APPLICATION = 'Application'
    ACTION_EXIT = 'Exit'
    MESSAGE_BOX_TITLE = 'Exit'
    MESSAGE_BOX_QUESTION = 'Are you sure you want to quit?'
    WIDTH = 1000
    HEIGHT = 1200
    BACKGROUND_IMAGE = ':/images/cachexia.png'
    BACKGROUND_GRAY_RECT_R = 255
    BACKGROUND_GRAY_RECT_G = 255
    BACKGROUND_GRAY_RECT_B = 255
    BACKGROUND_GRAY_RECT_A = 64
    
    def __init__(self):
        super(MainWindow, self).__init__()
        action = QAction(MainWindow.ACTION_EXIT, self)
        action.triggered.connect(self._exitApplication)
        applicationMenu = QMenu(MainWindow.MENU_ITEM_APPLICATION)
        applicationMenu.addAction(action)
        self.menuBar().addMenu(applicationMenu)
        tabWidget = TabWidget(self.menuBar())
        self.menuBar().setNativeMenuBar(False)
        self.setCentralWidget(tabWidget)
        self.setFixedSize(QSize(MainWindow.WIDTH, MainWindow.HEIGHT))
        self.setWindowTitle(MainWindow.TITLE)
        self._centerWindow()

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

    def _exitApplication(self) -> None:
        choice = QMessageBox.question(
            self, MainWindow.MESSAGE_BOX_TITLE, MainWindow.MESSAGE_BOX_QUESTION, QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            QApplication.quit()

    def _centerWindow(self) -> None:
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))