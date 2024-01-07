import time

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class CheckDicomHeaderTask(Task):
    def __init__(self) -> None:
        super(CheckDicomHeaderTask, self).__init__()

    def run(self) -> None:
        # # Get parameters needed for this task
        # nrIterations = self.parameter('nrIterations').value()
        # canceled = False
        # for i in range(nrIterations):
        #     # Check if task was canceled first
        #     if self.statusIsCanceling():
        #         canceled = True
        #         break
        #     # Do your work and update progress based on nr. steps required
        #     LOGGER.info(f'DummyTask: iteration = {i}')
        #     self.setProgress(step=i, nrSteps=nrIterations)
        #     # Wait a bit
        #     time.sleep(1)
        # # Terminate task either canceled, error or finished
        # if canceled:
        #     self.setStatusCanceled()
        # elif self.hasErrors():
        #     self.setStatusError()
        # else:
        #     self.setStatusFinished()
        pass