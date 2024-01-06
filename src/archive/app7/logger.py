import os
import sys
import logging

from singleton import singleton
from utils import createNameWithTimestamp

LOGFILEPATH = os.environ.get('LOGFILEPATH', 'MosamaticDesktop.log')
if os.path.isfile(LOGFILEPATH):
    os.remove(LOGFILEPATH)
with open(LOGFILEPATH, 'w') as f:
    pass


@singleton
class Logger:
    def __init__(self) -> None:
        os.remove(LOGFILEPATH)
        self._logger = logging.getLogger('MosamaticDesktop')
        self._logger.addHandler(self.standardOutputHandler())
        self._logger.addHandler(self.fileOutputHandler())
        self.enableInfo()

    def standardOutputHandler(self) -> logging.StreamHandler:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        return handler
    
    def fileOutputHandler(self) -> logging.FileHandler:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(LOGFILEPATH)
        handler.setFormatter(formatter)
        return handler
    
    def logFilePath(self) -> str:
        print(f'Logger.logFilePath() {LOGFILEPATH}')
        return LOGFILEPATH
    
    def enableDebug(self) -> None:
        self._logger.setLevel(logging.DEBUG)
        for handler in self._logger.handlers:
            handler.setLevel(logging.DEBUG)

    def enableInfo(self) -> None:
        self._logger.setLevel(logging.INFO)
        for handler in self._logger.handlers:
            handler.setLevel(logging.INFO)
    
    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)