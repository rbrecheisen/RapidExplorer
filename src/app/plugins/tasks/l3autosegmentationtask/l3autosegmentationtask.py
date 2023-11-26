from PySide6.QtWidgets import QDialog

from barbell2_bodycomp import MuscleFatSegmentator, BodyCompositionCalculator
from barbell2_bodycomp.convert import npy2png, dcm2npy

from plugins.tasks.task import Task
from plugins.tasks.l3autosegmentationtask.l3autosegmentationtasksettingsdialog import L3AutoSegmentationTaskSettingsDialog
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class L3AutoSegmentationTask(Task):
    def __init__(self) -> None:
        super(L3AutoSegmentationTask, self).__init__(name='L3 Auto-Segmentation')
        self._taskSettingsDialog = None
        # TODO: Specify inputs and parameters to be passed to the settings dialog
        # Perhaps I can make a general settings dialog that works for all tasks?
        # In Mosamatic Web I do the same.
        self._outputData = None

    def showSettingsDialog(self) -> None:
        # TODO: Move this to parent task
        dialog = L3AutoSegmentationTaskSettingsDialog(task=self)
        resultCode = dialog.exec_()
        if resultCode == QDialog.Accepted:
            print('Input data: {}'.format(self.setting('inputData')))
            print('TensorFlow model files: {}'.format(self.setting('tensorFlowModelFiles')))
        elif resultCode == QDialog.Rejected:
            print('Dialog rejected')
        else:
            raise RuntimeError(f'Unknown return code {resultCode}')

    def run(self) -> None:
        inputData = self.data(name='inputData')
        print(inputData)

    def outputData(self) -> RegisteredMultiFileSetModel:
        return self._outputData