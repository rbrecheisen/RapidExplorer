import os
import shutil

from data.datamanager import DataManager
from tasks.taskmanager import TaskManager

INPUTFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/pancreasdemo')
TENSORFLOWMODELFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/tensorflowmodelfiles')
OUTPUTDIRECTORY = os.path.join(os.environ['HOME'], 'Desktop/downloads/pancreasdemo-output')


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
    # TODO: Standardize these setting names
    task.settings().setting(name='dicomFileSet').setValue(value=inputFileSet)
    task.settings().setting(name='tensorFlowModelFileSet').setValue(value=tensorFlowModelFileSet)
    task.settings().setting(name='outputFileSetDirectory').setValue(value=OUTPUTDIRECTORY)
    outputFileSet = taskManager.runCurrentTask(task, background=False)
    assert len(outputFileSet.files()) == 4

def taskProgress(progress: int):
    print(f'Task progress: {progress}')

def taskFinished():
    print('Task finished')