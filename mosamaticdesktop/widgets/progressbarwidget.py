from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.singleton import singleton


@singleton
class ProgressBarWidget(QProgressBar):
    def __init__(self) -> None:
        super(ProgressBarWidget, self).__init__()