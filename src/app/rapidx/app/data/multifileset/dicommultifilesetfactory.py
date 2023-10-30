import os
import pydicom
import pydicom.errors

from typing import List

from rapidx.app.data.db import Db
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.fileset.dicomfilesetfactory import DicomFileSetFactory
from rapidx.app.data.factory import Factory
from rapidx.app.data.file.dicomfile import DicomFile


class DicomMultiFileSetFactory(Factory):
    def __init__(self) -> None:
        super(DicomMultiFileSetFactory, self).__init__()
        self._nrFiles = 0
        self._progress = 0

    def create(self, multiFileSetModel: MultiFileSetModel, db: Db) -> List[List[DicomFile]]:
        data = {}
        self._progress = 0
        for root, dirs, files in os.walk(multiFileSetModel.path()):
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
        i = 0
        # TODO: How to deal with progress updates?
        dicomMultiFileSets = []
        for fileSetPath in data.keys():
            fileSetName = os.path.relpath(fileSetPath, multiFileSetModel.path())
            fileSetModel = FileSetModelFactory.create(multiFileSetModel=multiFileSetModel, name=fileSetName, path=fileSetPath)
            db.add(fileSetModel)
            factory = DicomFileSetFactory()
            factory.signal().progress.connect(self._updateProgress)
            dicomFileSet = factory.create(fileSetModel=fileSetModel, db=db)
            dicomMultiFileSets.append(dicomFileSet)
        return dicomMultiFileSets
    
    def _updateProgress(self, progress) -> None:
        self._progress = int((i + 1) / self._nrFiles * 100)
