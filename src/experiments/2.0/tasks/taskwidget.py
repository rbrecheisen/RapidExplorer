import inspect

from PySide6.QtWidgets import QWidget

from tasks.task import Task
from tasks.taskwidgetexception import TaskWidgetException
from logger import Logger

LOGGER = Logger()


class TaskWidget(QWidget):    
    # Trick to return the child class name when NAME is retrieved
    # https://chat.openai.com/c/b7bd6334-5ec3-40e3-9af1-93405c68d795
    @classmethod
    def NAME(cls):
        return cls.__qualname__[:-6]
    
    def __init__(self, taskType: Task) -> None:
        super(TaskWidget, self).__init__()
        if not inspect.isclass(taskType):
            raise TaskWidgetException('TaskWidget: argument taskType should be a class')
        self._taskType = taskType
        self._task = None

    def name(self) -> str:
        return self.__class__.__name__
    
    # Execution

    def startTask(self) -> None:
        self._task = self._taskType()
        LOGGER.info('TaskWidget: running task...')
        self._task.start()

    def cancelTask(self) -> None:
        if self._task:
            LOGGER.info('TaskWidget: cancelling task...')
            self._task.setStatusCanceling()
        else:
            raise TaskWidgetException('TaskWidget: cannot cancel task, start it first')
        
    # Status
        
    def taskIsIdle(self) -> bool:
        if self._task:
            return self._task.statusIsIdle()
        raise TaskWidgetException('TaskWidget: cannot determine task idle status, start it first')
        
    def taskIsStart(self) -> bool:
        if self._task:
            return self._task.statusIsStart()
        raise TaskWidgetException('TaskWidget: cannot determine task start status, start it first')
        
    def taskIsRunning(self) -> bool:
        if self._task:
            return self._task.statusIsRunning()
        raise TaskWidgetException('TaskWidget: cannot determine task running status, start it first')
        
    def taskIsCanceling(self) -> bool:
        if self._task:
            return self._task.statusIsCanceling()
        raise TaskWidgetException('TaskWidget: cannot determine task canceled status, start it first')
        
    def taskIsCanceled(self) -> bool:
        if self._task:
            return self._task.statusIsCanceled()
        raise TaskWidgetException('TaskWidget: cannot determine task canceled status, start it first')
        
    def taskIsFinished(self) -> bool:
        if self._task:
            return self._task.statusIsFinished()
        raise TaskWidgetException('TaskWidget: cannot determine task finished status, start it first')
    
    def taskIsError(self) -> bool:
        if self._task:
            return self._task.statusIsError()
        raise TaskWidgetException('TaskWidget: cannot determine task error status, start it first')