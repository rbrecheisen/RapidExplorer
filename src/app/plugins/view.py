from PySide6.QtWidgets import QWidget


class View(QWidget):
    def __init__(self) -> None:
        super(View, self).__init__()

    def setData(self, data) -> None:
        raise NotImplementedError('Not implemented')