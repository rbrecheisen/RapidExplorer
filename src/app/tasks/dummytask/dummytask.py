import time

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__()

    def run(self) -> None:
        nrIterations = self.parameter('nrIterations').value()
        canceled = False        
        for i in range(nrIterations):
            if self.statusIsCanceling():
                canceled = True
                break
            LOGGER.info(f'DummyTask: iteration = {i}')
            self.setProgress(step=i, nrSteps=nrIterations)
            time.sleep(1)
        if canceled:
            self.setStatusCanceled()
        else:
            self.setStatusFinished()