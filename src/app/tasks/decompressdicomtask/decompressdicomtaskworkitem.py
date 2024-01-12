import pydicom
import pydicom.errors

from tasks.taskworkitem import TaskWorkItem
from tasks.taskworkitemexception import TaskWorkItemException


class DecompressDicomTaskWorkItem(TaskWorkItem):
    def __init__(self, inputFilePath: str, outputFilePath: str) -> None:
        super(DecompressDicomTaskWorkItem, self).__init__()
        self._inputFilePath = inputFilePath
        self._outputFilePath = outputFilePath

    def execute(self) -> None:
        try:
            p = pydicom.dcmread(self._inputFilePath)
            p.decompress()
            p.save_as(self._outputFilePath)
        except pydicom.errors.InvalidDicomError:
            raise TaskWorkItemException(f'Skipping non-DICOM: {self._inputFilePath}')
