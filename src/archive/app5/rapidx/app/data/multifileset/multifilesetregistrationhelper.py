import os
import pydicom

from rapidx.app.data.db.db import Db
from rapidx.app.data.registrationhelper import RegistrationHelper
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.db.dbaddcommand import DbAddCommand


class MultiFileSetRegistrationHelper(RegistrationHelper):
    def __init__(self, name: str, path: str, db: Db) -> None:
        super(MultiFileSetRegistrationHelper, self).__init__(name=name, path=path, db=db)
        self._nrFiles = 0

    def nrFiles(self) -> int:
        return self._nrFiles
    
    def execute(self) -> MultiFileSetModel:
        data = {}
        self._nrFiles = 0
        for root, dirs, files in os.walk(self.path()):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                try:
                    pydicom.dcmread(filePath, stop_before_pixels=True)
                    if root not in data.keys():
                        data[root] = []
                    data[root].append(filePath)
                    self._nrFiles += 1
                except pydicom.errors.InvalidDicomError:
                    print(f'File {fileName} is not a valid DICOM file')
                    continue
        multiFileSetModel = MultiFileSetModel(name=self.name(), path=self.path())
        for fileSetPath in data.keys():
            fileSetName = os.path.relpath(fileSetPath, multiFileSetModel.path)
            fileSetModel = FileSetModel(multiFileSetModel, name=fileSetName, path=fileSetPath)
            fileSetModel = DbAddCommand(self.db(), FileSetModel, fileSetModel).execute()
        multiFileSetModel = DbAddCommand(self.db(), MultiFileSetModel, multiFileSetModel).execute()
        return multiFileSetModel
