import os
import pytest

from rapidx.app.data.multifileset.dicommultifilesetimporter import DicomMultiFileSetImporter


MULTIFILESETMODELNAME = 'myMultiFileSet'
MULTIFILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset')

progress = 0


@pytest.mark.long_running
def test_importDicomMultiFileSetAndCheckInFileCache(db):
    def updateProgress(value):
        global progress
        progress = value

    def importFinished(value):
        assert value

    importer = DicomMultiFileSetImporter(path=MULTIFILESETMODELPATH, db=db)
    importer.signal().progress.connect(updateProgress)
    importer.signal().finished.connect(importFinished)
    importer.run()
    multiFileSetModel = importer.data()
    assert multiFileSetModel.id