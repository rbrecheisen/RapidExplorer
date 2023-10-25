import os

from sqlalchemy.orm import Session
from typing import List

from rapidx.tests.data.fileset.filesetmodel import FileSetModel
from rapidx.tests.data.file.filemodelfactory import FileModelFactory
from rapidx.tests.data.file.dicomfilefactory import DicomFileFactory
from rapidx.tests.data.file.dicomfile import DicomFile


class DicomFileSetFactory:
    @staticmethod
    def create(fileSetModel: FileSetModel, session: Session) -> List[DicomFile]:
        files = os.listdir(fileSetModel.path())
        nrFiles = len(files)
        i = 0
        dicomFileSet = []
        for f in files:
            fileName = f
            filePath = os.path.join(fileSetModel.path(), fileName)
            fileModel = FileModelFactory.create(fileSetModel=fileSetModel, path=filePath)
            session.add(fileModel)
            try:
                dicomFile = DicomFileFactory.create(fileModel=fileModel)
                dicomFileSet.append(dicomFile)
                print('.', end='', flush=True)
            except DicomFileInvalidException:
                print(f'\nFile {fileName} is not a valid DICOM file')
                continue
        session.commit()
        dicomFileSet.sort(key=lambda x: int(x.data().InstanceNumber))
        return dicomFileSet
