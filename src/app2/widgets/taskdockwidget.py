from PySide6.QtWidgets import QDockWidget, QTextEdit
from widgets.dockwidget import Dockwidget


class TaskDockWidget(Dockwidget):
    def __init__(self, title: str, minWidth: int, maxWidth) -> None:
        super(TaskDockWidget, self).__init__(title)
        self.setMinimumWidth(minWidth)
        self.setMaximumHeight(maxWidth)
        self.setWidget(QTextEdit('Place holder for tasks'))
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)