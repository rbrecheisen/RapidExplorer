import time

from tasks.taskworkitem import TaskWorkItem
from logger import Logger

LOGGER = Logger()


class DummyTaskWorkItem(TaskWorkItem):
    def __init__(self) -> None:
        super(DummyTaskWorkItem, self).__init__()

    def execute(self) -> None:
        LOGGER.info('Executing DummyTaskWorkItem...')
        time.sleep(1)