import os
import pydicom
import pydicom.errors

from typing import List

from rapidx.app.data.db.db import Db
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from app.rapidx.app.data.fileset.dicomfilesetloader import DicomFileSetLoader
from rapidx.app.data.factory import Factory
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.db.dbaddcommand import DbAddCommand


class DicomMultiFileSetLoader(Factory):
    def __init__(self) -> None:
        super(DicomMultiFileSetLoader, self).__init__()
        self._i = 0
        self._nrFiles = 0
        self._progress = 0

    def execute(self, multiFileSetModel: MultiFileSetModel, db: Db) -> List[List[DicomFile]]:
        # data = {}
        # for root, dirs, files in os.walk(multiFileSetModel.path):
        #     for fileName in files:
        #         filePath = os.path.join(root, fileName)
        #         try:
        #             pydicom.dcmread(filePath, stop_before_pixels=True)
        #             if root not in data.keys():
        #                 data[root] = []
        #             data[root].append(filePath)
        #             self._nrFiles += 1
        #         except pydicom.errors.InvalidDicomError:
        #             print(f'File {fileName} is not a valid DICOM file')
        #             continue
        # # # Connect only finished signal. Don't connect the update progress signal because
        # # # this signal is sent out by the DicomFileSetFactory objects
        # # self.signal().finished.connect(self._importFinished)
        # dicomFileSets = []
        # for fileSetPath in data.keys():
        #     fileSetName = os.path.relpath(fileSetPath, multiFileSetModel.path)
        #     fileSetModel = FileSetModel(multiFileSetModel, name=fileSetName, path=fileSetPath)
        #     fileSetModel = DbAddCommand(db, FileSetModel, fileSetModel).execute()
        dicomFileSets = []
        for fileSetModel in multiFileSetModel.fileSetModels():
            loader = DicomFileSetLoader()
            loader.signal().progress.connect(self._updateProgress)
            dicomFileSet = loader.execute(fileSetModel=fileSetModel, db=db)
            dicomFileSets.append(dicomFileSet)
        self.signal().finished.emit(True)
        return dicomFileSets
    
    def _updateProgress(self, progress) -> None:
        self._progress = int((self._i + 1) / self._nrFiles * 100)
        self.signal().progress.emit(self._progress)
        self._i += 1
