import time

from tasks.task import Task
from data.datamanager import DataManager
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__()

    def run(self) -> None:

        canceled = False
        manager = DataManager()

        # Get parameters needed for this task
        nrIterations = self.parameter('nrIterations').value()

        # Do iterations of the task
        for i in range(nrIterations):
            
            # Check if task was canceled first
            if self.statusIsCanceling():
                canceled = True
                break

            # ==> Do file processing here...

            # Update progress based on nr. steps required. This will automatically
            # send sigals/events to the task widget
            self.updateProgress(step=i, nrSteps=nrIterations)

            # If necessary wait a bit
            time.sleep(1)

        # Terminate task either canceled, error or finished
        if canceled:
            self.setStatusCanceled()
        elif self.hasErrors():
            self.setStatusError()
        else:
            self.setStatusFinished()