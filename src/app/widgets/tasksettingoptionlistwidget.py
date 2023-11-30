from PySide6.QtWidgets import QWidget, QComboBox


class TaskSettingOptionListWidget(QComboBox):
    def __init__(self, parent: QWidget=None) -> None:
        super(TaskSettingOptionListWidget, self).__init__(parent=parent)