from abc import ABC

from PySide6.QtWidgets import QDockWidget


class Dockwidget(QDockWidget):
    def __init__(self, title: str) -> None:
        super(Dockwidget, self).__init__(title)