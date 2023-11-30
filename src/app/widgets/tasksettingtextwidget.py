from PySide6.QtWidgets import QWidget, QLineEdit


class TaskSettingTextWidget(QLineEdit):
    def __init__(self, parent: QWidget=None) -> None:
        super(TaskSettingTextWidget, self).__init__(parent=parent)