import os
import sys
import logging

from typing import List

from mosamaticdesktop.singleton import singleton
from mosamaticdesktop.utils import createNameWithTimestamp

LOGFILEPATH = os.environ.get('LOGFILEPATH', 'MosamaticDesktop.log')


@singleton
class Logger:
    def __init__(self) -> None:
        if os.path.isfile(LOGFILEPATH):
            os.remove(LOGFILEPATH)
        with open(LOGFILEPATH, 'w') as f:
            pass
        self._logger = logging.getLogger('MosamaticDesktop')
        self._logger.addHandler(self.standardOutputHandler())
        self._logger.addHandler(self.fileOutputHandler())
        # This prevent logging to be propagated up to the root logger
        # which TensorFlow might reconfigure
        self._logger.propagate = False 
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
    
    def logHandlers(self) -> List[logging.Handler]:
        return self._logger.handlers
    
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

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)