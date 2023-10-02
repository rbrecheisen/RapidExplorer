from PySide6.QtWidgets import QApplication
from com.application.mainwindow import MainWindow


def main():
    app = QApplication(['Rbeesoft RAPID'])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()


if __name__ == "__main__":
    main()
