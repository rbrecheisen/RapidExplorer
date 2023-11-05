import os

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfileimporter import DicomFileImporter


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')


def test_importDicomFileAndCheckInFileCache(db):
    def updateProgress(value):
        global progress
        progress = value

    def importFinished(value):
        assert value

    importer = DicomFileImporter(path=FILEMODELPATH, db=db)
    importer.signal().progress.connect(updateProgress)
    importer.signal().finished.connect(importFinished)
    importer.run()
    multiFileSetModel = importer.data()
    assert multiFileSetModel.id