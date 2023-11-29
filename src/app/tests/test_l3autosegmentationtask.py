import os

from data.datamanager import DataManager
from tasks.taskmanager import TaskManager

FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/pancreasdemo')
TENSORFLOWMODELFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/tensorflowmodelfiles')


def test_taskCanLoadInputData():

    # Load data
    dataManager = DataManager()
    inputFileSet = dataManager.createFileSetFromFileSetPath(fileSetPath=FILESETPATH)
    tensorFlowModelFileSet = dataManager.createFileSetFromFileSetPath(fileSetPath=TENSORFLOWMODELFILESETPATH)

    # Run task
    taskManager = TaskManager()
    taskManager.signal().taskProgress.connect(self.taskProgress)
    taskManager.signal().taskFinished.connect(self.taskFinished)
    taskManager.loadTasks()
    task = taskManager.task(name='L3AutoSegmentationTask')
    task.addInputFileSet(inputFileSet, 'dicomFiles')
    task.addInputFileSet(tensorFlowModelFileSet, 'tensorFlowModelFiles')
    taskManager.runTask(task)

def taskProgress(progress: int):
    pass

def taskFinished():
    pass