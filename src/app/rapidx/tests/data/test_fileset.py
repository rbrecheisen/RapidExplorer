import os
import pytest

from rapidx.app.data.fileset.dicomfilesetimporter import DicomFileSetImporter


FILESETMODELNAME = 'myFileSet'
FILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1')

progress = 0


@pytest.mark.long_running
def test_importDicomFileSetAndCheckInFileCache(db):
    def updateProgress(value):
        global progress
        progress = value

    def importFinished(value):
        assert value

    importer = DicomFileSetImporter(path=FILESETMODELPATH, db=db)
    importer.signal().progress.connect(updateProgress)
    importer.signal().finished.connect(importFinished)
    importer.run()
    multiFileSetModel = importer.data()
    assert multiFileSetModel.id