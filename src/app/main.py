import os
import sys

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from mainwindow import MainWindow


def main():
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
