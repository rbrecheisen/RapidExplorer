import time

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__()

    def run(self) -> None:
        self.setStatus(status=Task.RUNNING)
        LOGGER.info('DummyTask: running...')
        canceled = False        
        for i in range(10):
            LOGGER.info(f'DummyTask: processing step={i}')
            if self.status() == Task.CANCELLING:
                LOGGER.info('DummyTask: cancelling...')
                canceled = True
                break
            time.sleep(1)
        if canceled:
            self.setStatus(status=Task.CANCELED)
            LOGGER.info('DummyTask: canceled')
        else:
            self.setStatus(status=Task.FINISHED)
            LOGGER.info('DummyTask: finished')

    def cancel(self) -> None:
        self.setStatus(status=Task.CANCELLING)