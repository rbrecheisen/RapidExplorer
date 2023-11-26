from PySide6.QtWidgets import QDialog

from barbell2_bodycomp import MuscleFatSegmentator, BodyCompositionCalculator
from barbell2_bodycomp.convert import npy2png, dcm2npy

from plugins.tasks.task import Task
from plugins.tasks.tasktextsetting import TaskTextSetting
from app.plugins.tasks.taskfileselectorsetting import TaskFileSelectorSetting
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class L3AutoSegmentationTask(Task):
    def __init__(self) -> None:
        super(L3AutoSegmentationTask, self).__init__(name='L3 Auto-Segmentation')
        self.addSetting(TaskFileSelectorSetting(name='inputData', displayName='Input Data'))
        self.addSetting(TaskFileSelectorSetting(name='tensorFlowModelFiles', displayName='TensorFlow Model Files'))
        self.addSetting(TaskTextSetting(name='outputDataName', displayName='Output Data Name (optional)'))
        self._outputData = None

    def run(self) -> None:
        inputData = self.data(name='inputData')
        print(inputData)

    def outputData(self) -> RegisteredMultiFileSetModel:
        return self._outputData