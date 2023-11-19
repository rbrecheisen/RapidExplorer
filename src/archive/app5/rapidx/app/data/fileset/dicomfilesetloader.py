import os

from typing import List

from rapidx.app.data.db.db import Db
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.file.dicomfileloader import DicomFileLoader
from rapidx.app.data.loader import Loader
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.db.dbgetcommand import DbGetCommand
from rapidx.app.data.db.dbfilterbycommand import DbFilterByCommand
from rapidx.app.data.file.dicomfileinvalidexception import DicomFileInvalidException


class DicomFileSetLoader(Loader):
    def __init__(self, fileSetModel: FileSetModel, db: Db) -> None:
        super(DicomFileSetLoader, self).__init__()
        self._fileSetModel = fileSetModel
        self._db = db
        # self._nrFiles = nrFiles

    def execute(self) -> List[DicomFile]:
        i = 0
        dicomFileSet = []
        fileSetModel = DbGetCommand(self._db, FileSetModel, self._fileSetModel.unboundId).execute()
        fileModels = DbFilterByCommand(self._db, FileModel, fileSetModelId=fileSetModel.id).execute()
        for fileModel in fileModels:
            loader = DicomFileLoader(fileModel, db=self._db)
            loader.signal().progress.connect(self._updateProgress)
            dicomFile = loader.execute()
            dicomFileSet.append(dicomFile)
            # progress = int((i + 1) / self._nrFiles * 100)

            # Emit a signal that another progress step has been made. We don't
            # need to emit the actual progress value because the parent
            # DicomMultiFileSetLoader keeps track of progress already
            # self.signal().progress.emit(1)
            print('.', end='', flush=True)
            i += 1
        dicomFileSet.sort(key=lambda x: int(x.data().InstanceNumber))
        self.signal().finished.emit(True)
        return dicomFileSet
    
    def _updateProgress(self, progress) -> None:
        print(f'DicomFileSetLoader.progress = {progress}')
        self.signal().progress.emit(1)
    
        # files = os.listdir(fileSetModel.path)
        # nrFiles = len(files)
        # i = 0
        # dicomFileSet = []
        # for f in files:
        #     fileName = f
        #     filePath = os.path.join(fileSetModel.path, fileName)
        #     fileModel = FileModel(fileSetModel, path=filePath)
        #     fileModel = DbAddCommand(db, FileModel, fileModel).execute()
        #     try:
        #         dicomFile = DicomFileFactory().create(fileModel=fileModel)
        #         dicomFileSet.append(dicomFile)
        #         print('.', end='', flush=True)
        #     except DicomFileInvalidException:
        #         print(f'\nFile {fileName} is not a valid DICOM file')
        #         continue
        #     progress = int((i + 1) / nrFiles * 100)
        #     self.signal().progress.emit(progress)
        #     i += 1
        # dicomFileSet.sort(key=lambda x: int(x.data().InstanceNumber))
        # self.signal().finished.emit(True)
        return dicomFileSet
