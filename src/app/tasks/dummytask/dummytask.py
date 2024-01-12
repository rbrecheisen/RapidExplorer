import time

from typing import List

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__()

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