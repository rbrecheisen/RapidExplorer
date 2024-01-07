from tasks.task import Task
from data.datamanager import DataManager
from logger import Logger

LOGGER = Logger()


class DecompressDicomTask(Task):
    def __init__(self) -> None:
        super(DecompressDicomTask, self).__init__()

    def run(self) -> None:
        canceled = False
        manager = DataManager()

        # Prepare parameters, then run task
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = manager.fileSetByName(inputFileSetName)
        if inputFileSet is not None:
            outputFileSetPath = self.parameter('outputFileSetPath').value()
            outputFileSetName = self.parameter('outputFileSetName').value()
            if outputFileSetName is None:
                outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
            overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        else:
            self.addError(f'Input fileset {inputFileSetName} does not exist')

        # Determine task final status
        if canceled:
            self.setStatusCanceled()
        elif self.hasErrors():
            self.setStatusError()
        else:
            self.setStatusFinished()