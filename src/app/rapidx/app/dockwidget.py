from PySide6.QtWidgets import QDockWidget


class Dockwidget(QDockWidget):
    def __init__(self, title: str, parent=None) -> None:
        super(Dockwidget, self).__init__(title, parent=parent)

    # TODO: add maximize buttons (see ChatGPT suggestions)