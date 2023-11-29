import os
import shutil

from data.datamanager import DataManager
from tasks.taskmanager import TaskManager

INPUTFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/pancreasdemo')
OUTPUTDIRECTORY = os.path.join(os.environ['HOME'], 'Desktop/downloads/pancreasdemo-output')
TENSORFLOWMODELFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/tensorflowmodelfiles')


def test_taskCanLoadInputData():

    if os.path.isdir(OUTPUTDIRECTORY):
        shutil.rmtree(OUTPUTDIRECTORY)

    # Load data
    dataManager = DataManager()
    inputFileSet = dataManager.importFileSet(fileSetPath=INPUTFILESETPATH)
    tensorFlowModelFileSet = dataManager.importFileSet(fileSetPath=TENSORFLOWMODELFILESETPATH)

    # Run task
    taskManager = TaskManager()
    taskManager.signal().taskProgress.connect(taskProgress)
    taskManager.signal().taskFinished.connect(taskFinished)
    taskManager.loadTasks()
    task = taskManager.task(name='MuscleFatSegmentationTask')
    task.settings().setting(name='dicomFiles').setValue(value=inputFileSet)
    task.settings().setting(name='tensorFlowModelFiles').setValue(value=tensorFlowModelFileSet)
    task.settings().setting(name='outputFileSetDirectory').setValue(value=OUTPUTDIRECTORY)
    outputFileSet = taskManager.runTask(task, background=False)
    assert len(outputFileSet.files()) == 4

def taskProgress(progress: int):
    print(f'Task progress: {progress}')

def taskFinished():
    print('Task finished')