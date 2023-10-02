from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


class Tab(QWidget):

    FONT_COLOR = 'white'
    LABEL_ALIGNMENT = Qt.AlignCenter

    def __init__(self) -> None:
        super(Tab, self).__init__()
