import os
import pydicom
import pydicom.errors

from typing import List

from rapidx.app.data.db.db import Db
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.fileset.dicomfilesetloader import DicomFileSetLoader
from rapidx.app.data.loader import Loader
from rapidx.app.data.file.dicomfile import DicomFile
from rapidx.app.data.db.dbcountchildrencommand import DbCountChildrenCommand


class DicomMultiFileSetLoader(Loader):
    def __init__(self, multiFileSetModel: MultiFileSetModel, db: Db) -> None:
        super(DicomMultiFileSetLoader, self).__init__(), 
        self._multiFileSetModel = multiFileSetModel
        self._db = db
        # self._nrFiles = nrFiles
        self._progress = 0
        self._i = 0

    def execute(self) -> List[List[DicomFile]]:
        dicomFileSets = []
        for fileSetModel in self._multiFileSetModel.fileSetModels:
            loader = DicomFileSetLoader(fileSetModel, db=self._db)
            loader.signal().progress.connect(self._updateProgress)
            dicomFileSet = loader.execute()
            dicomFileSets.append(dicomFileSet)
        # Emit a signal that this DicomMultiFileSetLoader is finished. This will be
        # picked up by the parent DicomMultiFileSetImporter object
        self.signal().finished.emit(True)
        return dicomFileSets
    
    def _updateProgress(self, progress) -> None:
        # Each progress step of the DicomFileSetLoader objects executed while result in 
        # a call to this method. Another progress signal will be emitted to the parent 
        # DicomMultiFileSetImporter object.
        # self._progress = int((self._i + 1) / self._nrFiles * 100)
        # print(f'DicomMultiFileSetLoader.progress = {self._progress}')
        # self.signal().progress.emit(self._progress)
        self.signal().progress.emit(50)
        self._i += 1

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
