import os

from singleton import singleton


@singleton
class Configuration:
    def __init__(self) -> None:
        self._configDirectory = os.path.join(os.getenv('HOME'), '.mosamatic')

    def configDirectory(self) -> str:
        return self._configDirectory
    
    def taskConfigDirectory(self, taskName: str) -> str:
        taskConfigDirectory = os.path.join(self._configDirectory, taskName)
        if not os.path.isdir(taskConfigDirectory):
            os.makedirs(taskConfigDirectory, exist_ok=False)
        return taskConfigDirectory
    
    def taskConfigSubDirectory(self, taskName: str, dirName: str) -> str:
        taskConfigDirectory = self.taskConfigDirectory(taskName=taskName)
        taskConfigSubDirectory = os.path.join(taskConfigDirectory, dirName)
        if not os.path.isdir(taskConfigSubDirectory):
            os.makedirs(taskConfigSubDirectory, exist_ok=False)
        return taskConfigSubDirectory