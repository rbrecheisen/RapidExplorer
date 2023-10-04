from PySide6.QtWidgets import QDockWidget, QTextEdit
from widgets.dockwidget import Dockwidget


class LogDockWidget(Dockwidget):
    def __init__(self, title: str) -> None:
        super(LogDockWidget, self).__init__(title)
        self.setWidget(QTextEdit('Place holder for logs'))
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)