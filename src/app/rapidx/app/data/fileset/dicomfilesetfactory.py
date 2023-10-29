import os

from typing import List

from rapidx.app.data.db import Db
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.file.filemodelfactory import FileModelFactory
from rapidx.app.data.file.dicomfilefactory import DicomFileFactory
from rapidx.app.data.file.dicomfile import DicomFile


class DicomFileSetFactory:
    @staticmethod
    def create(fileSetModel: FileSetModel, db: Db) -> List[DicomFile]:
        files = os.listdir(fileSetModel.path())
        nrFiles = len(files)
        i = 0
        dicomFileSet = []
        for f in files:
            fileName = f
            filePath = os.path.join(fileSetModel.path(), fileName)
            fileModel = FileModelFactory.create(fileSetModel=fileSetModel, path=filePath)
            db.add(fileModel)
            try:
                dicomFile = DicomFileFactory.create(fileModel=fileModel)
                dicomFileSet.append(dicomFile)
                print('.', end='', flush=True)
            except DicomFileInvalidException:
                print(f'\nFile {fileName} is not a valid DICOM file')
                continue
        db.commit()
        dicomFileSet.sort(key=lambda x: int(x.data().InstanceNumber))
        return dicomFileSet
