from PySide6.QtWidgets import QWidget, QDoubleSpinBox


class TaskSettingFloatingPointWidget(QDoubleSpinBox):
    def __init__(self, parent: QWidget=None) -> None:
        super(TaskSettingFloatingPointWidget, self).__init__(parent=parent)

    def setRange(self, minimum: float, maximum: float) -> None:
        self.setRange(minimum, maximum)