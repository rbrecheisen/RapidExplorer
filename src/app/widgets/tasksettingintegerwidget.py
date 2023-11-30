from PySide6.QtWidgets import QWidget, QSpinBox


class TaskSettingIntegerWidget(QSpinBox):
    def __init__(self, parent: QWidget=None) -> None:
        super(TaskSettingIntegerWidget, self).__init__(parent=parent)

    def setRange(self, minimum: int, maximum: int) -> None:
        self.setRange(minimum, maximum)