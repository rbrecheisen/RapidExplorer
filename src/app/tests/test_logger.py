from logger import Logger
from utils import createNameWithTimestamp


def test_LoggerCanGenerateInfoButNotDebugLogging():
    infoMessage = f'INFO logging message: {createNameWithTimestamp()}'
    debugMessage = f'DEBUG logging message: {createNameWithTimestamp()}'
    logger = Logger()
    logger.info(infoMessage)
    logger.debug(debugMessage)
    infoMessageFound = False
    debugMessageFound = False
    with open(logger.logFilePath()) as f:
        lines = f.readlines()
        for line in lines:
            if infoMessage in line:
                infoMessageFound = True
            if debugMessage in line:
                debugMessageFound = True
    assert infoMessageFound and not debugMessageFound


def test_LoggerCanGenerateDebugLogging():
    infoMessage = f'INFO logging message: {createNameWithTimestamp()}'
    debugMessage = f'DEBUG logging message: {createNameWithTimestamp()}'
    logger = Logger()
    logger.enableDebug()
    logger.info(infoMessage)
    logger.debug(debugMessage)
    infoMessageFound = False
    debugMessageFound = False
    with open(logger.logFilePath()) as f:
        lines = f.readlines()
        for line in lines:
            if infoMessage in line:
                infoMessageFound = True
            if debugMessage in line:
                debugMessageFound = True
    assert infoMessageFound and debugMessageFound
