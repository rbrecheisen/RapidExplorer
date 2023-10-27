import os
import pytest

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.multifileset.dicommultifilesetimporter import DicomMultiFileSetImporter


MULTIFILESETMODELNAME = 'myMultiFileSet'
MULTIFILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset')


@pytest.mark.long_running
def test_importDicomMultiFileSetAndCheckInFileCache(session):
    importer = DicomMultiFileSetImporter(name=MULTIFILESETMODELNAME, path=MULTIFILESETMODELPATH, session=session)
    importer.run()
    dicomFileSets = importer.data()
    assert dicomFileSets
    assert len(dicomFileSets) > 0
    assert len(dicomFileSets[0]) > 0
    for dicomFileSet in dicomFileSets:
        for dicomFile in dicomFileSet:
            assert dicomFile.id()
            assert dicomFile.data()
            assert dicomFile.header()
            assert dicomFile.header(attributeName='SeriesDescription')
            assert dicomFile.pixelData().shape == (512, 512)
            # Check model associations
            assert dicomFile.fileModel().fileSetModel()
            assert dicomFile.fileModel().fileSetModel().multiFileSetModel()
            assert dicomFile.fileModel().fileSetModel().multiFileSetModel().name() == MULTIFILESETMODELNAME
            cache = FileCache()
            assert cache.get(dicomFile.id())
