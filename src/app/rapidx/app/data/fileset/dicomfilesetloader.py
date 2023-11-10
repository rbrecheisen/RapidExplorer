import os

from typing import List

from rapidx.app.data.db.db import Db
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.file.dicomfileloader import DicomFileLoader
from rapidx.app.data.loader import Loader
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.db.dbaddcommand import DbAddCommand
from rapidx.app.data.file.dicomfileinvalidexception import DicomFileInvalidException


class DicomFileSetLoader(Loader):
    def __init__(self, fileSetModel: FileSetModel) -> None:
        super(DicomFileSetLoader, self).__init__()
        self._fileSetModel = fileSetModel

    def execute(self) -> List[DicomFile]:
        nrFiles = len(self._fileSetModel.fileModels)
        i = 0
        dicomFileSet = []
        for fileModel in self._fileSetModel.fileModels:
            loader = DicomFileLoader(fileModel)
            dicomFile = loader.execute()
            dicomFileSet.append(dicomFile)
            progress = int((i + 1) / nrFiles * 100)
            self.signal().progress.emit(progress)
            print('.', end='', flush=True)
            i += 1
        dicomFileSet.sort(key=lambda x: int(x.data().InstanceNumber))
        return dicomFileSet
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
