from PySide6.QtWidgets import QWidget


class View(QWidget):
    def __init__(self) -> None:
        super(View, self).__init__()

    def addData(self, data, name) -> None:
        raise NotImplementedError('Not implemented')
    
    # TODO: Remove this method
    def setData(self, data) -> None:
        raise NotImplementedError('Not implemented')