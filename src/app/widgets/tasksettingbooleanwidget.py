from PySide6.QtWidgets import QWidget, QComboBox


class TaskSettingBooleanWidget(QComboBox):
    def __init__(self, parent: QWidget=None) -> None:
        super(TaskSettingBooleanWidget, self).__init__(parent=parent)
        self.addItems([None, 'True', 'False'])