import time

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__()

    def run(self) -> None:
        # Get parameters needed for this task
        nrIterations = self.parameter('nrIterations').value()
        canceled = False
        errors = []
        for i in range(nrIterations):
            # Check if task was canceled first
            if self.statusIsCanceling():
                canceled = True
                break
            # Do you work and update progress based on nr. steps required
            LOGGER.info(f'DummyTask: iteration = {i}')
            self.setProgress(step=i, nrSteps=nrIterations)
            # Wait awhile (may not be necessary)
            time.sleep(1)
        # Terminate task either canceled or finished
        if canceled:
            self.setStatusCanceled()
        else:
            self.setStatusFinished()