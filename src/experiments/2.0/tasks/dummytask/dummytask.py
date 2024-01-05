import time

from tasks.task import Task
from logger import Logger

LOGGER = Logger()


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__(name='DummyTask')

    def run(self) -> None:
        self.setStatus(status=Task.RUNNING)
        LOGGER.info('Running dummy task (takes about 5 seconds)...')
        canceled = False        
        for i in range(10):
            LOGGER.info(f'Iteration: {i}')
            if self.status() == Task.CANCELLING:
                LOGGER.info('Cancelling task...')
                canceled = True
                break
            time.sleep(1)
        if canceled:
            self.setStatus(status=Task.CANCELED)
            LOGGER.info('Task canceled')
        else:
            self.setStatus(status=Task.FINISHED)
            LOGGER.info('Task finished')

    def cancel(self) -> None:
        self.setStatus(status=Task.CANCELLING)