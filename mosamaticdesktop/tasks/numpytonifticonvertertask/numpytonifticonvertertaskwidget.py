from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.numpytonifticonvertertask.numpytonifticonvertertask import NumPyToNiftiConverterTask


class NumPyToNiftiConverterTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(NumPyToNiftiConverterTaskWidget, self).__init__(taskType=NumPyToNiftiConverterTask, progressBar=progressBar)

    def validate(self) -> None:
        pass