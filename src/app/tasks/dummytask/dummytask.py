import time

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__()

    def run(self) -> None:
        canceled = False        
        for i in range(10):
            if self.statusIsCanceling():
                canceled = True
                break
            LOGGER.info(f'DummyTask: processing step={i}')
            time.sleep(1)
        if canceled:
            self.setStatusCanceled()
        else:
            self.setStatusFinished()