import os
import pydicom
import pydicom.errors

from typing import List

from rapidx.app.data.db import Db
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.fileset.dicomfilesetfactory import DicomFileSetFactory
from rapidx.app.data.file.dicomfile import DicomFile


class DicomMultiFileSetFactory:
    @staticmethod
    def create(multiFileSetModel: MultiFileSetModel, db: Db) -> List[List[DicomFile]]:
        data = {}
        nrFiles = 0
        for root, dirs, files in os.walk(multiFileSetModel.path()):
            for fileName in files:
                filePath = os.path.join(root, fileName)
                try:
                    pydicom.dcmread(filePath, stop_before_pixels=True)
                    if root not in data.keys():
                        data[root] = []
                    data[root].append(filePath)
                    nrFiles += 1
                except pydicom.errors.InvalidDicomError:
                    print(f'File {fileName} is not a valid DICOM file')
                    continue
        i = 0
        dicomMultiFileSets = []
        for fileSetPath in data.keys():
            fileSetName = os.path.relpath(fileSetPath, multiFileSetModel.path())
            fileSetModel = FileSetModelFactory.create(multiFileSetModel=multiFileSetModel, name=fileSetName, path=fileSetPath)
            db.add(fileSetModel)
            dicomFileSet = DicomFileSetFactory.create(fileSetModel=fileSetModel, db=db)
            dicomMultiFileSets.append(dicomFileSet)
        return dicomMultiFileSets
