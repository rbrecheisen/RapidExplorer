from PySide6.QtWidgets import QDockWidget, QTextEdit
from widgets.dockwidget import Dockwidget


class LogDockWidget(Dockwidget):
    def __init__(self, title: str, minHeight: int, maxHeight: int) -> None:
        super(LogDockWidget, self).__init__(title)
        self.setWidget(QTextEdit('Place holder for logs'))
        self.setMinimumHeight(minHeight)
        self.setMaximumHeight(maxHeight)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
