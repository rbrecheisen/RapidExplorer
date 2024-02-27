import time

from typing import List

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    """
    This is an example task that you can copy to implement your own tasks. 
    The following methods are available from the base Task class:

        - self.parameter(name)
        - parameterValuesAsString()
        - self.dataManager()
        - self.addInfo(message)
        - self.addError(message)
        - self.addWarning(message)
        - self.updateProgress(step, nrSteps)
        - self.readFromCache(file))
        - self.writeToCache(file, fileObject)
        - self.generateTimestampForFileSetName(name)
    """
    def __init__(self) -> None:
        super(DummyTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='This is some description of the dummy task'
        )
        self.addIntegerParameter(
            name='nrIterations', 
            labelText='Nr. Iterations',
            optional=False,
            visible=True,
            defaultValue=10,
            minimum=0,
            maximum=100,
            step=1,
        )

    def execute(self) -> None:

        # Get parameters needed for this task
        nrIterations = self.parameter('nrIterations').value()
        
        # Do iterations of the task
        for i in range(nrIterations):
        
            # Check if task was canceled first
            if self.statusIsCanceled():
                self.addInfo('Canceling task...')
                break

            # Do your processing here...
            self.addInfo(f'Processing iteration {i}/{nrIterations}')

            # Update progress based on nr. steps required. This will automatically
            # send sigals/events to the task widget
            self.updateProgress(step=i, nrSteps=nrIterations)

            # If necessary wait a bit
            time.sleep(1)